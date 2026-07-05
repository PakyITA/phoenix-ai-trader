class PhoenixAiTraderPanel extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <style>
        iframe {
          width: 100%;
          height: 100vh;
          border: 0;
        }
      </style>

      <iframe src="/local/phoenix/index.html?v=${Date.now()}"></iframe>
    `;
  }
}

customElements.define("phoenix-ai-trader-panel", PhoenixAiTraderPanel);
