
const getList = async () => {
  let url = 'http://127.0.0.1:5000/produtos';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.produtos.forEach(item => insertList(item.nome, item.quantidade, item.valor))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

getList()


const postItem = async (inputProduct, inputQuantity, inputPrice) => {
  const formData = new FormData();
  formData.append('nome', inputProduct);
  formData.append('quantidade', inputQuantity);
  formData.append('valor', inputPrice);

  let url = 'http://127.0.0.1:5000/produto';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7"); // Botão 'X'
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}



const setupEditMode = (row, editCell) => { // Deve receber 'editCell'
  
  let editButton = document.createElement("button");
  editButton.textContent = "Editar";
  editButton.className = "editBtn"; 
  
  // Adiciona o botão diretamente na célula de edição fornecida
  editCell.appendChild(editButton); 

  editButton.onclick = function () {
    let nameCell = row.cells[0];   
    let qtyCell = row.cells[1];    
    let priceCell = row.cells[2];  

    const originalName = nameCell.textContent;

    if (editButton.textContent === "Editar") {
      // Modo Edição
      qtyCell.innerHTML = `<input type='text' value='${qtyCell.textContent}' class='editInput'>`;
      priceCell.innerHTML = `<input type='text' value='${priceCell.textContent}' class='editInput'>`;
      editButton.textContent = "Salvar";
    } else {
      // Modo Salvar
      let newQty = qtyCell.querySelector('input').value;
      let newPrice = priceCell.querySelector('input').value;

      if (isNaN(newQty) || isNaN(newPrice) || newQty === '' || newPrice === '') {
        alert("Quantidade e Valor devem ser números e não podem estar vazios.");
        return;
      }

      updateItem(originalName, newQty, newPrice);

      qtyCell.innerHTML = newQty;
      priceCell.innerHTML = newPrice;
      editButton.textContent = "Editar";
    }
  };
};

const removeElement = () => {
  let close = document.getElementsByClassName("close");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement; // div é a linha <tr>
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/produto?nome=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


const updateItem = async (originalName, newQuantity, newPrice) => {
  const formData = new FormData();
  formData.append('quantidade', newQuantity);
  formData.append('valor', newPrice);

  let url = 'http://127.0.0.1:5000/produto?nome=' + originalName;
  fetch(url, {
    method: 'put',
    body: formData
  })
    .then((response) => response.json())
    .then(() => alert("Item atualizado!"))
    .catch((error) => {
      console.error('Error:', error);
      alert("Erro ao atualizar item.");
    });
}


const newItem = () => {
  let inputProduct = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputProduct === '') {
    alert("Escreva o nome de um item!");
  } else if (isNaN(inputQuantity) || isNaN(inputPrice)) {
    alert("Quantidade e valor precisam ser números!");
  } else {
    insertList(inputProduct, inputQuantity, inputPrice)
    postItem(inputProduct, inputQuantity, inputPrice)
    alert("Item adicionado!")
  }
}


const insertList = (nameProduct, quantity, price) => {
  var item = [nameProduct, quantity, price]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  // Insere as células de dados (Nome, Qtd, Valor)
  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }

  // --- A CORREÇÃO ESTÁ AQUI ---
  // 1. Cria a célula de EDIÇÃO (4ª coluna)
  var editCell = row.insertCell(-1);
  
  // 2. Cria a célula de REMOÇÃO (5ª coluna)
  var deleteCell = row.insertCell(-1);
  
  // 3. Adiciona o botão "X" na CÉLULA DE REMOÇÃO
  insertButton(deleteCell);
  
  // 4. Adiciona o botão "Editar" na CÉLULA DE EDIÇÃO
  setupEditMode(row, editCell);
  // --- FIM DA CORREÇÃO ---

  // Limpa os inputs do formulário
  document.getElementById("newInput").value = "";
  document.getElementById("newQuantity").value = "";
  document.getElementById("newPrice").value = "";

  // Ativa o botão de remover
  removeElement();
}