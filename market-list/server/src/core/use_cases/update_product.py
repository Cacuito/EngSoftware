# Em src/core/use_cases/update_product.py

from src.core.entities.product import Product
from src.core.interfaces.product_repository import ProductRepository
from src.core.exceptions import ProductNotFound 

class UpdateProductUseCase:
    """Implementa o caso de uso para atualizar um produto."""
    
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(
        self, 
        original_name: str, 
        new_name: str, 
        new_quantity: int, 
        new_value: float
    ) -> Product:
        """
        Executa a lógica de atualização (nome, qtd e valor).
        """
        
        # 1. Encontra o produto pelo nome original
        produto = self.repository.get_by_name(original_name) 
        
        if not produto:
            raise ProductNotFound("Produto não encontrado")
            
        # 2. Atualiza todos os dados do objeto
        produto.nome = new_name 
        produto.quantidade = new_quantity
        produto.valor = new_value
        
        # 3. Salva o objeto 'produto' atualizado (que agora tem o novo nome)
        updated_produto = self.repository.update(produto)
        
        return updated_produto