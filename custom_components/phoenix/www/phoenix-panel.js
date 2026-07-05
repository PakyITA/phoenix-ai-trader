class PhoenixAiTraderPanel extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <iframe
        src="/phoenix_ai_trader/index.html?v=021"
        style="border:0;width:100%;height:100vh;">
      </iframe>
    `;
  }
}

customElements.define("phoenix-ai-trader-panel", PhoenixAiTraderPanel);
