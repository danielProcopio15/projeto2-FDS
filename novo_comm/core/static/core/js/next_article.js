document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('next-article-button');
    if (!btn) return;

    async function loadPreview() {
        const currentId = btn.getAttribute('data-current-id');
        const apiUrl = `/api/next-article/${currentId}/`;

        try {
            const res = await fetch(apiUrl, { headers: { 'Accept': 'application/json' } });
            if (!res.ok) throw new Error('No next');
            const data = await res.json();

            btn.querySelector('.next-category').textContent = data.category || '';
            btn.querySelector('.next-title').textContent = data.title || 'Próxima matéria';
            const img = btn.querySelector('.next-thumb img');
            if (data.image_url) img.src = data.image_url;
            btn.dataset.detailUrl = data.detail_url;
            btn.dataset.nextId = data.id;
        } catch (err) {
            // esconder botão se não houver próxima matéria
            btn.style.opacity = '0';
            btn.style.pointerEvents = 'none';
        }
    }

    async function navigateToNext() {
        const detailUrl = btn.dataset.detailUrl;
        const nextId = btn.dataset.nextId;
        if (!detailUrl) return;

        try {
            // busca o HTML parcial da nova matéria
            const res = await fetch(detailUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            if (!res.ok) throw new Error('fetch failed');
            const text = await res.text();

            // Substitui o conteúdo do artigo sem recarregar a página inteira
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            const newArticle = doc.querySelector('#article-content');
            const currentArticle = document.querySelector('#article-content');
            if (newArticle && currentArticle) {
                currentArticle.innerHTML = newArticle.innerHTML;
                // Atualiza título da página e URL no histórico
                const newTitle = doc.querySelector('title');
                if (newTitle) document.title = newTitle.textContent;
                window.history.pushState({}, '', detailUrl);
                // atualiza o botão para a próxima recomendação
                btn.setAttribute('data-current-id', nextId);
                loadPreview();
                // rola para o topo do artigo para melhor experiência
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        } catch (err) {
            console.error('Navegação falhou', err);
            // fallback: redireciona para a página normal
            window.location.href = btn.dataset.detailUrl;
        }
    }

    btn.addEventListener('click', (e) => {
        e.preventDefault();
        navigateToNext();
    });

    // Carrega a primeira prévia
    loadPreview();

    // Atualiza quando voltar no histórico
    window.addEventListener('popstate', () => {
        // tenta recarregar preview com o id atual (se encontrar no DOM)
        const current = document.querySelector('#article-content');
        if (current && current.dataset && current.dataset.articleId) {
            btn.setAttribute('data-current-id', current.dataset.articleId);
        }
        loadPreview();
    });
});
