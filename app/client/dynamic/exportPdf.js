async function exportAnalyticsToPDF() {
  try {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF('p', 'mm', 'a4');
    const margin = 15;
    const pageWidth = pdf.internal.pageSize.getWidth() - 2 * margin;
    let yPosition = margin;

    const graphSections = document.querySelectorAll('.graph');

    for (const section of graphSections) {
      if (section.querySelector('#exportPdfBtn')) continue;

      // Клонируем секцию
      const clone = section.cloneNode(true);

      // Копируем содержимое canvas из оригинала в клон
      const originalCanvases = section.querySelectorAll('canvas');
      const cloneCanvases = clone.querySelectorAll('canvas');

      for (let i = 0; i < originalCanvases.length; i++) {
        const originalCanvas = originalCanvases[i];
        const cloneCanvas = cloneCanvases[i];
        if (!cloneCanvas) continue;

        const dataURL = originalCanvas.toDataURL();

        const ctx = cloneCanvas.getContext('2d');
        const img = new Image();
        await new Promise(resolve => {
          img.onload = () => {
            ctx.clearRect(0, 0, cloneCanvas.width, cloneCanvas.height);
            ctx.drawImage(img, 0, 0);
            resolve();
          };
          img.src = dataURL;
        });
      }

      // Изменяем цвет заголовков в клоне
      clone.querySelectorAll('h2, h3').forEach(h => {
        h.style.color = '#111'; // Можно заменить на нужный цвет
      });

      clone.style.position = 'absolute';
      clone.style.left = '-9999px';
      clone.style.top = '0';
      clone.style.backgroundColor = '#fff';
      document.body.appendChild(clone);

      const canvas = await html2canvas(clone, {
        scale: 2,
        logging: false,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        ignoreElements: el => el.id === 'exportPdfBtn',
      });

      document.body.removeChild(clone);

      const imgData = canvas.toDataURL('image/png');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfHeight = (imgProps.height * pageWidth) / imgProps.width;

      if (yPosition + pdfHeight > pdf.internal.pageSize.getHeight() - margin) {
        pdf.addPage();
        yPosition = margin;
      }

      pdf.addImage(imgData, 'PNG', margin, yPosition, pageWidth, pdfHeight);
      yPosition += pdfHeight + 15;
    }

    pdf.save('financial-analytics-report.pdf');

  } catch (error) {
    console.error('PDF generation error:', error);
    alert('Ошибка при создании отчёта: ' + error.message);
  }
}

// Инициализация кнопки с проверкой загрузки библиотек
document.addEventListener('DOMContentLoaded', function() {
  let exportBtn = document.getElementById('exportPdfBtn');
  if (exportBtn) {
    const newExportBtn = exportBtn.cloneNode(true);
    exportBtn.parentNode.replaceChild(newExportBtn, exportBtn);
    exportBtn = newExportBtn;

    exportBtn.addEventListener('click', async function() {
      if (!window.jspdf || !window.html2canvas) {
        alert('Библиотеки для экспорта не загружены. Пожалуйста, обновите страницу.');
        return;
      }

      exportBtn.disabled = true;
      exportBtn.textContent = 'Генерация PDF...';

      try {
        await exportAnalyticsToPDF();
      } catch (e) {
        console.error(e);
        alert('Ошибка при генерации: ' + e.message);
      } finally {
        exportBtn.disabled = false;
        exportBtn.textContent = 'Скачать отчет в PDF';
      }
    });
  }
});