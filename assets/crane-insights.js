(() => {
  const tooltip = document.createElement('div');
  tooltip.className = 'chartTooltip';
  tooltip.hidden = true;
  document.body.appendChild(tooltip);

  function showTooltip(target, text) {
    tooltip.textContent = text;
    tooltip.hidden = false;
    const box = target.getBoundingClientRect();
    const left = Math.min(window.innerWidth - tooltip.offsetWidth - 10, Math.max(10, box.left + box.width / 2));
    const top = Math.max(10, box.top - tooltip.offsetHeight - 8);
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
  }

  function hideTooltip() {
    tooltip.hidden = true;
  }

  document.querySelectorAll('.insightColumnGroup i').forEach((bar) => {
    const chart = bar.closest('.insightColumns');
    const label = bar.dataset.label || '';
    const value = bar.dataset.value || '';
    const activate = () => {
      chart?.classList.add('is-active');
      bar.classList.add('is-active');
      showTooltip(bar, `${label}: ${value}`);
    };
    const deactivate = () => {
      chart?.classList.remove('is-active');
      bar.classList.remove('is-active');
      hideTooltip();
    };
    bar.addEventListener('mouseenter', activate);
    bar.addEventListener('focus', activate);
    bar.addEventListener('mouseleave', deactivate);
    bar.addEventListener('blur', deactivate);
  });

  document.querySelectorAll('.insightDonut li').forEach((item) => {
    const activate = () => showTooltip(item, item.textContent.replace(/\s+/g, ' ').trim());
    item.addEventListener('mouseenter', activate);
    item.addEventListener('focus', activate);
    item.addEventListener('mouseleave', hideTooltip);
    item.addEventListener('blur', hideTooltip);
  });

  const lightbox = document.createElement('dialog');
  lightbox.className = 'insightLightbox';
  lightbox.innerHTML = '<button type="button" class="insightLightboxClose" aria-label="关闭">&times;</button><img alt=""><div class="insightLightboxMeta"><p class="insightLightboxCaption"></p><p class="insightLightboxQuality" hidden></p></div>';
  document.body.appendChild(lightbox);
  const lightboxImage = lightbox.querySelector('img');
  const lightboxCaption = lightbox.querySelector('.insightLightboxCaption');
  const lightboxQuality = lightbox.querySelector('.insightLightboxQuality');
  const closeLightbox = () => lightbox.close();
  lightbox.querySelector('.insightLightboxClose').addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.querySelectorAll('.insightImageButton').forEach((button) => {
    button.addEventListener('click', () => {
      const isEnglish = document.documentElement.dataset.language === 'en';
      const caption = isEnglish
        ? (button.dataset.captionEn || button.dataset.caption || '')
        : (button.dataset.captionZh || button.dataset.caption || '');
      const qualityNote = isEnglish
        ? (button.dataset.qualityNoteEn || '')
        : (button.dataset.qualityNoteZh || '');
      lightboxImage.src = button.dataset.fullSrc || '';
      lightboxImage.alt = caption;
      lightboxCaption.textContent = caption;
      lightboxQuality.textContent = qualityNote;
      lightboxQuality.hidden = !qualityNote;
      lightbox.classList.toggle('sourceLow', Boolean(qualityNote));
      lightbox.showModal();
    });
  });
})();
