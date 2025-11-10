# -*- coding: utf-8 -*-
"""Teste simples do sistema de recomendacao"""

from core.recommendation import update_session_access, get_session_access_data, get_user_recommendation

# Simula sessao Django
class MockSession:
    def __init__(self):
        self.data = {}
        self.modified = False
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __setitem__(self, key, value):
        self.data[key] = value
        self.modified = True
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __contains__(self, key):
        return key in self.data

# Teste basico
session = MockSession()

# Simular acessos
update_session_access(session, 'Cultura')
update_session_access(session, 'Cultura')  
update_session_access(session, 'Esportes')
update_session_access(session, 'Esportes')
update_session_access(session, 'Esportes')

# Ver dados
access_data = get_session_access_data(session)
print("Dados da sessao:")
for category, info in access_data.items():
    print(f"  {category}: {info['count']} acessos")

# Testar recomendacao
recommended = get_user_recommendation(session, is_authenticated=False)
print(f"\nCategoria recomendada: {recommended}")

if recommended == 'Esportes':
    print("SUCESSO! Funciona para usuarios nao logados!")
else:
    print(f"Resultado inesperado: {recommended}")