async function exportDashboardToPDF() {
  try {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF('p', 'mm', 'a4');
    const margin = 15;
    const pageWidth = pdf.internal.pageSize.getWidth() - 2 * margin;
    let yPosition = margin;

    // Выбираем блоки для экспорта (cards и graph, кроме кнопки)
    const exportBlocks = document.querySelectorAll('.cards, .graph');

    for (const block of exportBlocks) {
      // Пропускаем кнопку в блоке graph
      if (block.querySelector('#exportPdfBtn')) continue;

      const canvas = await html2canvas(block, {
        scale: 2,
        logging: false,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        ignoreElements: el => el.id === 'exportPdfBtn',
      });

      const imgData = canvas.toDataURL('image/png');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfHeight = (imgProps.height * pageWidth) / imgProps.width;

      if (yPosition + pdfHeight > pdf.internal.pageSize.getHeight() - margin) {
        pdf.addPage();
        yPosition = margin;
      }

      pdf.addImage(imgData, 'PNG', margin, yPosition, pageWidth, pdfHeight);
      yPosition += pdfHeight + 10;
    }

    pdf.save('financial-dashboard-report.pdf');
  } catch (error) {
    console.error('Ошибка при создании PDF:', error);
    alert('Ошибка при создании отчёта: ' + error.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const exportBtn = document.getElementById('exportPdfBtn');
  if (!exportBtn) return;

  exportBtn.addEventListener('click', async () => {
    if (!window.jspdf || !window.html2canvas) {
      alert('Библиотеки для экспорта не загружены. Пожалуйста, обновите страницу.');
      return;
    }

    exportBtn.disabled = true;
    exportBtn.textContent = 'Генерация PDF...';

    try {
      await exportDashboardToPDF();
    } catch (e) {
      console.error(e);
      alert('Ошибка при генерации: ' + e.message);
    } finally {
      exportBtn.disabled = false;
      exportBtn.textContent = 'Скачать отчет в PDF';
    }
  });
});