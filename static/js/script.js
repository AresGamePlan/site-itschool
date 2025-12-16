document.addEventListener('DOMContentLoaded', () => {
  const langSelect = document.getElementById('languege');
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      const newLang = e.target.value;
      // сохраняем выбранный язык в cookie на 30 дней
      document.cookie = `lang=${newLang};path=/;max-age=${60 * 60 * 24 * 30}`;
      // обновляем страницу, чтобы подгрузились переводы
      location.reload();
    });
  }
});
// Если жизнь тебе посылает задачу которую не возможно решить без JavaScript чтоб было просто и локонично,
// УЛЫБНИСЬ и разьеби монитор)))