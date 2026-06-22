# Checklist De Publicação

Rode antes de publicar uma nova versão:

```powershell
.\scripts\validate.ps1 -BasePath "/projeto_retro" -SiteUrl "https://marcusguedess.github.io/projeto_retro"
```

Verificações manuais:

- As screenshots do README refletem a interface atual.
- `web/out/index.html` e `web/out/.nojekyll` existem após o build.
- Não há CSV privado, chave de API, log local ou cache no repositório.
- GitHub Pages está configurado para usar GitHub Actions.
- A demonstração pública usa dados de amostra ou dados com permissão de publicação.
