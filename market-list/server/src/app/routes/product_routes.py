# Em src/app/routes/product_routes.py

from urllib.parse import unquote

from flask_openapi3 import Tag
from src.app.schemas import (
    ErrorSchema,
    ListagemProdutosSchema,
    ProdutoBuscaPorNomeSchema,
    ProdutoBuscaSchema,
    ProdutoDelSchema,
    ProdutoSchema,  # Espera o Schema completo
    ProdutoViewSchema,
    apresenta_produto,
    apresenta_produtos,
    # Você não precisa mais do ProdutoUpdateSchema
)
from src.core.exceptions import ProductAlreadyExists, ProductNotFound
from src.core.use_cases.add_product import AddProductUseCase
from src.core.use_cases.delete_product import DeleteProductUseCase
from src.core.use_cases.get_product import GetProductUseCase
from src.core.use_cases.list_products import ListProductsUseCase
from src.core.use_cases.update_product import UpdateProductUseCase 

produto_tag = Tag(
    name="Produto",
    description="Adição, visualização, atualização e remoção de produtos à base",
)


def register_product_routes(
    app,
    add_use_case: AddProductUseCase,
    list_use_case: ListProductsUseCase,
    get_use_case: GetProductUseCase,
    delete_use_case: DeleteProductUseCase,
    update_use_case: UpdateProductUseCase, 
) -> None:
    
    # Rota POST (Adicionar)
    @app.post(
        "/produto",
        tags=[produto_tag],
        responses={
            "200": ProdutoViewSchema,
            "409": ErrorSchema,
            "400": ErrorSchema,
        },
    )
    def add_produto(form: ProdutoSchema):
        try:
            produto = add_use_case.execute(
                form.nome, form.quantidade, form.valor
            )
            return apresenta_produto(produto), 200
        except ProductAlreadyExists as error:
            return {"mesage": str(error)}, 409
        except Exception:
            return {"mesage": "Não foi possível salvar novo item :/"}, 400

    # Rota GET (Listar Todos)
    @app.get(
        "/produtos",
        tags=[produto_tag],
        responses={"200": ListagemProdutosSchema, "404": ErrorSchema},
    )
    def get_produtos():
        produtos = list_use_case.execute()
        if not produtos:
            return {"produtos": []}, 200
        return apresenta_produtos(produtos), 200

    # Rota GET (Buscar Um)
    @app.get(
        "/produto",
        tags=[produto_tag],
        responses={"200": ProdutoViewSchema, "404": ErrorSchema},
    )
    def get_produto(query: ProdutoBuscaSchema):
        try:
            produto = get_use_case.execute(query.id)
            return apresenta_produto(produto), 200
        except ProductNotFound as error:
            return {"mesage": str(error)}, 404

    # Rota PUT (Atualizar)
    @app.put(
        "/produto",
        tags=[produto_tag],
        responses={
            "200": ProdutoViewSchema,
            "404": ErrorSchema,
            "400": ErrorSchema
        },
    )
    def update_produto(query: ProdutoBuscaPorNomeSchema, form: ProdutoSchema):
        """Atualiza os dados de um produto existente na base."""
        
        nome_original = unquote(unquote(query.nome))
        
        try:
            # Passa todos os novos dados (incluindo o novo nome) para o caso de uso
            produto_atualizado = update_use_case.execute(
                original_name=nome_original,
                new_name=form.nome,
                new_quantity=form.quantidade,
                new_value=form.valor
            )
            return apresenta_produto(produto_atualizado), 200
        
        except ProductNotFound as error:
            return {"mesage": str(error)}, 404
        except Exception as e:
            return {"mesage": f"Não foi possível atualizar o item: {e}"}, 400

    # Rota DELETE (Remover)
    @app.delete(
        "/produto",
        tags=[produto_tag],
        responses={"200": ProdutoDelSchema, "404": ErrorSchema},
    )
    def del_produto(query: ProdutoBuscaPorNomeSchema):
        nome = unquote(unquote(query.nome))
        try:
            delete_use_case.execute(nome)
            return {"mesage": "Produto removido", "nome": nome}, 200
        except ProductNotFound as error:
            return {"mesage": str(error)}, 404