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
        new_quantity: int, 
        new_value: float
    ) -> Product:
        """
        Executa a lógica de atualização (só qtd e valor).
        """
        
        # 1. Encontra o produto
        produto = self.repository.get_by_name(original_name) 
        
        if not produto:
            raise ProductNotFound("Produto não encontrado")
            
        # 2. Atualiza os dados do objeto
        produto.quantidade = new_quantity
        produto.valor = new_value
        
        # 3. Salva no banco
        updated_produto = self.repository.update(produto)
        
        return updated_produto