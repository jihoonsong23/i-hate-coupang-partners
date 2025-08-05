async function checkLink(){
  const url = document.getElementById('urlInput').value;

  const res = await fetch('https://your-backend-url/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({url})
  });

  const data = await res.json();

  const resultDiv = document.getElementById('result');
  if(data.error){
    resultDiv.innerHTML = `<p>오류: ${data.error}</p>`;
  }else{
    resultDiv.innerHTML = `
      <p><strong>원본 URL:</strong> <a href="${data.final_url}" target="_blank">${data.final_url}</a></p>
      <p><strong>파트너스 여부:</strong> ${data.is_partners ? '✅ 파트너스 링크' : '❌ 일반 링크'}</p>
      <p><strong>파트너스 ID:</strong> ${data.partners_id}</p>
    `;
  }
}
