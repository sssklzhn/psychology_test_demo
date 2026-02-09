// Простой роутер для SPA
export class Router {
    constructor(routes) {
        this.routes = routes;
        this.currentPage = null;
        
        // Обработчик изменения hash
        window.addEventListener('hashchange', () => this.handleRouteChange());
        
        // Обработчик загрузки страницы
        window.addEventListener('load', () => this.handleRouteChange());
    }
    
    handleRouteChange() {
        const hash = window.location.hash.slice(1) || '/';
        const route = this.routes[hash] || this.routes['/'];
        
        if (route) {
            // Уничтожаем текущую страницу если есть
            if (this.currentPage && this.currentPage.destroy) {
                this.currentPage.destroy();
            }
            
            // Рендерим новую страницу
            const app = document.getElementById('app');
            if (app) {
                app.innerHTML = '';
                this.currentPage = new route.page(this);
                const pageElement = this.currentPage.render();
                if (pageElement) {
                    app.appendChild(pageElement);
                }
            }
        }
    }
    
    navigate(path) {
        window.location.hash = path;
    }
    
    getCurrentPath() {
        return window.location.hash.slice(1) || '/';
    }
}