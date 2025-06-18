pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

const showPDF = document.querySelector('.showPDF')
const downloadBtn = document.querySelector('.downloadPDF')
let translatedTextGlobal = ''

document.querySelector('.targetPdf').addEventListener('change', (event) => {
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
        showPDF.src = e.target.result
    }
    reader.readAsDataURL(file)
})

document.querySelector('.translatePDF').addEventListener('click', async () => {
    const file = document.querySelector('.targetPdf').files[0]
    const language = document.querySelector('.selectLang').value
    const output = document.querySelector('.temp-body')

    if(!file) return alert('Please select a pdf file to translate')
    
    try{

        const pdfData = await file.arrayBuffer()
        const pdfDoc = await pdfjsLib.getDocument({ data: pdfData }).promise
        let textContent = ' ';

        for(let i = 1; i <= pdfDoc.numPages; i++){
            const page = await pdfDoc.getPage(i);
            const text = await page.getTextContent();
            text.items.forEach(item => textContent += item.str + ' ');

        }

        if (!textContent.trim()) return (output.textContent = 'No text found in PDF.');

        let translatedText = await translateTextInChunks(textContent, language);
        // Sanitize translated text by removing non-printable characters
        translatedText = translatedText.replace(/[^\x20-\x7E\n\r]+/g, '');
        translatedTextGlobal = translatedText;

        output.innerHTML = createStruturedText(translatedTextGlobal);

        downloadBtn.disabled = false;

    }catch(err){
        console.error('Error', err);
        output.textContent = 'There went something wrong!';
    }
});

downloadBtn.addEventListener('click', () => {
    if (!translatedTextGlobal) {
        alert('No translated text available to download.');
        return;
    }
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const pageHeight = doc.internal.pageSize.height;
    const margin = 10;
    const maxLineWidth = doc.internal.pageSize.width - margin * 2;
    const lineHeight = 10;
    let y = margin;

    // Use splitTextToSize for proper text wrapping
    const lines = doc.splitTextToSize(translatedTextGlobal, maxLineWidth);

    lines.forEach((line) => {
        if (y + lineHeight > pageHeight - margin) {
            doc.addPage();
            y = margin;
        }
        doc.text(line, margin, y);
        y += lineHeight;
    });

    doc.save('translated.pdf');
});

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const translateTextInChunks = async (text, lang) => {
    const chunkSize = 500, aprURL = 'https://api.mymemory.translated.net/get'
    let translated = ''
    const maxRetries = 5;

    for(let i = 0; i < text.length; i += chunkSize){
        const chunk = text.slice(i, i + chunkSize);
        let retries = 0;
        while (retries < maxRetries) {
            const res = await fetch(`${aprURL}?q=${encodeURIComponent(chunk)}&langpair=en|${lang}`);
            if(res.ok) {
                const data = await res.json();
                translated += data.responseData.translatedText;
                break;
            } else if (res.status === 429) {
                retries++;
                const delay = Math.pow(2, retries) * 1000; // exponential backoff
                console.warn(`Rate limited. Retry ${retries} in ${delay}ms`);
                await sleep(delay);
            } else {
                throw new Error(`Translation failed ${res.status}`);
            }
        }
        if (retries === maxRetries) {
            throw new Error('Max retries reached due to rate limiting');
        }
        // Delay between requests to avoid hitting rate limit
        await sleep(500);
    }

    console.log(translated)

    return translated;
}

const createStruturedText = (text) => text
    .split(/(?:\n+|\.\s*)/)
    .filter(section => section.trim())
    .map(section => `<p>${section.trim()}</p>`)
    .join('');
