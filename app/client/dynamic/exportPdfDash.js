async function exportDashboardToPDF() {
  try {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF('p', 'mm', 'a4');
    const margin = 15;
    const pageWidth = pdf.internal.pageSize.getWidth() - 2 * margin;
    let yPosition = margin;

    const exportBlocks = document.querySelectorAll('.cards, .graph');

    for (const block of exportBlocks) {
      if (block.querySelector('#exportPdfBtn')) continue;

      const clone = block.cloneNode(true);

      // Копируем содержимое canvas из оригинала в клон
      const originalCanvases = block.querySelectorAll('canvas');
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

      // Меняем цвет заголовков в клоне
      clone.querySelectorAll('h2, h3').forEach(h => {
        h.style.color = '#111';
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
      yPosition += pdfHeight + 10;
    }

    pdf.save('financial-dashboard-report.pdf');
  } catch (error) {
    console.error('Ошибка при создании PDF:', error);
    alert('Ошибка при создании отчёта: ' + error.message);
  }
}


// 👉 ВРЕМЕННО применить стили и вернуть старые
function applyTemporaryHeadingStyles() {
  const headings = document.querySelectorAll('.graph h2, .cards h3');
  const originalStyles = [];

  headings.forEach(h => {
    originalStyles.push({
      element: h,
      style: {
        color: h.style.color,
        backgroundColor: h.style.backgroundColor,
        fontWeight: h.style.fontWeight,
        padding: h.style.padding,
        borderRadius: h.style.borderRadius,
        display: h.style.display
      }
    });

    h.style.color = '#1a1a1a';
    h.style.fontWeight = 'bold';
    h.style.backgroundColor = '#f8f8f8';
    h.style.padding = '6px 10px';
    h.style.borderRadius = '6px';
    h.style.display = 'inline-block';
  });

  return originalStyles;
}

// 👉 ВОССТАНОВИТЬ стили после PDF
function restoreHeadingStyles(styles) {
  styles.forEach(({ element, style }) => {
    element.style.color = style.color;
    element.style.backgroundColor = style.backgroundColor;
    element.style.fontWeight = style.fontWeight;
    element.style.padding = style.padding;
    element.style.borderRadius = style.borderRadius;
    element.style.display = style.display;
  });
}

// 👉 Обработчик кнопки
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