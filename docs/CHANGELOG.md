# 📋 Changelog

Histórico de mudanças e versões do sistema de geração de boletos Cora.

## [2.0.0] - 2025-06-20

### 🚀 Adicionado
- **Estrutura de projeto completa** com organização em pastas específicas
- **Sistema de validações robusto** para CPF, CNPJ, email, CEP, datas e valores monetários
- **Testes automatizados** com pytest para validações e gerador
- **Documentação completa** com guias de API, configuração, exemplos e troubleshooting
- **Modo demonstração** para testes sem certificados reais
- **Logs detalhados** com configuração personalizável
- **Tratamento de erros** avançado com retry automático
- **Relatórios de geração** com estatísticas e detalhes
- **Integração com Excel** para geração em lote
- **Configuração via YAML** com validação automática

### 🔧 Melhorado
- **Autenticação mTLS** com cache de token otimizado
- **Validação de certificados** com verificação de permissões
- **Serialização JSON** para objetos dataclass
- **Estrutura de payload** padronizada
- **Tratamento de timeouts** e rate limiting
- **Organização de código** com separação clara de responsabilidades

### 🐛 Corrigido
- **Inicialização da classe CoraAuth** com parâmetro auth_url
- **Validação de CPF/CNPJ** com algoritmos oficiais
- **Formatação de valores monetários** em centavos
- **Validação de datas** com timezone UTC
- **Permissões de arquivos** para certificados
- **Estrutura do payload** nos testes

### 📚 Documentação
- **README.md** completo com instruções de instalação e uso
- **docs/API.md** com documentação detalhada da API Cora
- **docs/CONFIGURACAO.md** com guia de configuração passo a passo
- **docs/EXEMPLOS.md** com exemplos práticos de uso
- **docs/TROUBLESHOOTING.md** com solução de problemas comuns
- **docs/CHANGELOG.md** com histórico de versões

### 🧪 Testes
- **test_validacoes.py** para validações de dados
- **test_gerador.py** para testes do gerador de boletos
- **conftest.py** com configuração do pytest
- **tests/README.md** com documentação dos testes

## [1.5.0] - 2025-01-15

### 🚀 Adicionado
- **Sistema de autenticação mTLS** com certificados digitais
- **Geração de boletos individuais** com validação de dados
- **Integração básica com API Cora** v2
- **Estrutura de dataclasses** para validação de dados
- **Configuração via arquivo YAML**

### 🔧 Melhorado
- **Tratamento de erros** básico
- **Validação de dados** de entrada
- **Logs de execução** simples

### 🐛 Corrigido
- **Formatação de payload** para API
- **Validação de documentos** CPF/CNPJ
- **Tratamento de valores monetários**

## [1.0.0] - 2024-12-20

### 🚀 Adicionado
- **Versão inicial** do sistema
- **Estrutura básica** do projeto
- **Integração simples** com API Cora
- **Geração de boletos** básica
- **Configuração manual** de credenciais

### 🔧 Melhorado
- **Código base** funcional
- **Documentação inicial** básica

---

## 📊 Estatísticas da Versão 2.0

### Arquivos Criados/Modificados
- **Total de arquivos**: 25+
- **Linhas de código**: ~2000
- **Testes**: 15+ casos de teste
- **Documentação**: 6 arquivos MD

### Funcionalidades Implementadas
- ✅ Autenticação mTLS
- ✅ Validação de dados robusta
- ✅ Geração individual e em lote
- ✅ Testes automatizados
- ✅ Documentação completa
- ✅ Tratamento de erros
- ✅ Logs e relatórios
- ✅ Configuração flexível

### Compatibilidade
- **Python**: 3.8+
- **Sistemas**: Linux, Windows, macOS
- **APIs**: Cora v2
- **Formatos**: Excel, CSV, JSON

---

## 🔮 Roadmap Futuro

### Versão 2.1 (Planejada)
- [ ] **Interface web** para geração de boletos
- [ ] **Dashboard** com estatísticas em tempo real
- [ ] **Notificações automáticas** por email/SMS
- [ ] **Integração com webhooks** para status de pagamento
- [ ] **API REST** para integração externa

### Versão 2.2 (Planejada)
- [ ] **Sistema de templates** para boletos personalizados
- [ ] **Relatórios avançados** com gráficos
- [ ] **Backup automático** de certificados
- [ ] **Monitoramento** de performance
- [ ] **Integração com PIX** direto

### Versão 3.0 (Futuro)
- [ ] **Microserviços** para escalabilidade
- [ ] **Cache distribuído** com Redis
- [ ] **Filas de processamento** com Celery
- [ ] **Autenticação OAuth2** adicional
- [ ] **Interface mobile** para consultas

---

## 📝 Notas de Versão

### Migração da Versão 1.x para 2.0
1. **Backup** da configuração atual
2. **Atualizar** dependências do requirements.txt
3. **Migrar** config.yaml para nova estrutura
4. **Testar** com dados de exemplo
5. **Validar** certificados e permissões

### Breaking Changes
- **Estrutura de configuração** alterada
- **Nomes de classes** padronizados
- **Validações** mais rigorosas
- **Formato de payload** atualizado

### Deprecações
- **Configuração manual** de credenciais
- **Validações básicas** sem algoritmos oficiais
- **Logs simples** sem configuração

---

## 🤝 Contribuições

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Implemente** as mudanças
4. **Adicione** testes
5. **Documente** as alterações
6. **Submeta** um Pull Request

### Padrões de Código
- **PEP 8** para estilo Python
- **Type hints** para funções
- **Docstrings** para documentação
- **Testes** para novas funcionalidades
- **Logs** para debugging

---

## 📞 Suporte

### Versões Suportadas
- **Versão atual**: 2.0.0
- **Versão LTS**: 2.0.x
- **Versão anterior**: 1.5.x (suporte limitado)

### Contatos
- **Email**: suporte@cora.com.br
- **Documentação**: https://docs.cora.com.br
- **Issues**: GitHub Issues
- **Discord**: Comunidade Cora

---

**Última atualização**: Junho 2025
**Próxima versão**: 2.1.0 (Setembro 2025) 