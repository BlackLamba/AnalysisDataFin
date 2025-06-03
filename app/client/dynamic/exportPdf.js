async function exportAnalyticsToPDF() {
  try {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF('p', 'mm', 'a4');
    const margin = 15;
    const pageWidth = pdf.internal.pageSize.getWidth() - 2 * margin;
    let yPosition = margin;

    // Собираем все блоки графиков для экспорта
    const graphSections = document.querySelectorAll('.graph');

    // Рендерим каждый блок графика с его заголовком
    for (const section of graphSections) {
      // Пропускаем кнопку экспорта
      if (section.querySelector('#exportPdfBtn')) continue;

      // Рендерим весь блок графика как изображение
      const canvas = await html2canvas(section, {
        scale: 2,
        logging: false,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        ignoreElements: (element) => {
          // Игнорируем кнопку экспорта, если она есть в блоке
          return element.id === 'exportPdfBtn';
        }
      });

      const imgData = canvas.toDataURL('image/png');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfHeight = (imgProps.height * pageWidth) / imgProps.width;

      // Проверяем, помещается ли изображение на страницу
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
    // Заменяем кнопку на её клон, чтобы очистить все старые обработчики
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
