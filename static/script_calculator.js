// main.js
const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const num1 = parseFloat(form.num1.value);
    const num2 = parseFloat(form.num2.value);
    const operator = form.operator.value;

    let result;

    switch (operator) {
        case 'add':
            result = num1 + num2;
            break;
        case 'subtract':
            result = num1 - num2;
            break;
        case 'multiply':
            result = num1 * num2;
            break;
        case 'divide':
            result = num1 / num2;
            break;
    }

    const resultElement = document.createElement('div');
    resultElement.classList.add('result');
    resultElement.textContent = `Le résultat est : ${result}`;

    form.appendChild(resultElement);
});
