let storageMock = [
    { id: 1, name: "Молоко Простоквашино ультрапастеризованное 1,5%", price: 86.00, weight: 950, amount: 1, buy: "Купить" },
    { id: 2, name: "Творог Простоквашино мягкий 5%", price: 43.00, weight: 130, amount: 1, buy: "Купить" },
    { id: 3, name: "Сыр Брест-Литовск классический 45%", price: 185.00, weight: 200, amount: 1, buy: "Купить" },
    { id: 4, name: "Сметана Простоквашино из топленых сливок 15%", price: 69.00, weight: 260, amount: 1, buy: "Купить" },
    { id: 5, name: "Ряженка Домик в деревне 3,2%", price: 97.00, weight: 950, amount: 1, buy: "Купить" },
    { id: 6, name: "Кефир Экомилк 3,2%", price: 97.00, weight: 950, amount: 1, buy: "Купить" },];

let Cart = []
document.addEventListener("DOMContentLoaded", function () {
    fillStorageTable(storageMock);
});

function fillStorageTable(items) {
    let storageTable = document.getElementById('storage');

    items.forEach(e => {
        let itemTR = document.createElement('tr');
        itemTR.innerHTML = `<td>${e.id}</td><td>${e.name}</td><td>${e.price}</td><td>${e.weight}</td><td>${e.amount}</td><td>${e.buy}</td>`;
        storageTable.append(itemTR);
        itemTR.addEventListener('click', addToCart);
    });
};

Sum = 0;

function addToCart() {
    let cartTR = document.createElement("tr");
    cartTR.innerHTML = `<td>${this.childNodes[0].textContent}</td><td>${this.childNodes[1].textContent}</td><td>${this.childNodes[3].textContent}</td><td>${this.childNodes[4].textContent}</td><td>${this.childNodes[2].textContent}</td>`;
    document.getElementById('cart').append(cartTR);
    Sum += parseInt(this.childNodes[2].textContent.toString());
    document.getElementById('sum').innerHTML = Sum;
}