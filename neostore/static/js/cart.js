const USER_BALANCE = parseInt(
    document.getElementById('cart-config')?.dataset.balance || 0
);

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

function updateCartCount(count) {
    const cartCountSpan = document.getElementById('cart-count');

    if (cartCountSpan) {
        cartCountSpan.textContent = count;
        cartCountSpan.style.display =
            count > 0 ? 'inline-block' : 'none';
    }
}

function checkBalance(totalPrice) {
    const payLink = document.getElementById('PayBtn');
    const warningDiv = document.getElementById('warning-message');

    if (!payLink || !warningDiv) return;

    if (USER_BALANCE >= totalPrice) {
        payLink.classList.remove('btn-secondary', 'disabled');
        payLink.classList.add('btn-success');
        payLink.textContent = 'Оплатить';
        payLink.style.pointerEvents = 'auto';
        warningDiv.style.display = 'none';
    } else {
        payLink.classList.remove('btn-success');
        payLink.classList.add('btn-secondary', 'disabled');
        payLink.textContent = 'Недостаточно средств';
        payLink.style.pointerEvents = 'none';
        warningDiv.style.display = 'block';

        const needed = totalPrice - USER_BALANCE;

        warningDiv.innerHTML =
            `Недостаточно средств! Нужно ещё <strong>${needed}</strong> NeoCoins.<br>
            Ваш баланс: <strong>${USER_BALANCE}</strong> NeoCoins |
            Итого: <strong>${totalPrice}</strong> NeoCoins`;
    }
}

async function updateCartQuantity(thingId, quantity) {
    const response = await fetch(
        `/shop/update-cart-quantity/${thingId}/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quantity: quantity
            })
        }
    );

    return await response.json();
}

const payBtn = document.getElementById('PayBtn');

if (payBtn) {
    payBtn.addEventListener('click', async function (e) {
        e.preventDefault();

        const totalPrice = parseInt(
            document.getElementById('total-price').textContent
        );

        if (USER_BALANCE < totalPrice) {
            return;
        }

        const response = await fetch('/shop/checkout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            }
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = '/user/profile/';
        } else {
            alert(result.error || 'Ошибка оплаты');
        }
    });
}

document.querySelectorAll('.quantity-control').forEach(control => {

    const thingId = parseInt(control.dataset.id);

    const input = control.querySelector('.quantity-input');
    const decBtn = control.querySelector('.dec-btn');
    const incBtn = control.querySelector('.inc-btn');

    const card = control.closest('.card');

    const subtotalSpan = card.querySelector('.subtotal');

    const pricePerItem = parseInt(
        card.querySelector('.text-primary').textContent
    );

    async function updateDisplay(
        quantity,
        newSubtotal,
        newTotalPrice,
        cartCount,
        stockLeft
    ) {

        input.value = quantity;

        subtotalSpan.textContent = newSubtotal;

        document.getElementById('total-price').textContent =
            newTotalPrice;

        updateCartCount(cartCount);

        checkBalance(newTotalPrice);

        if (stockLeft <= 0) {
            incBtn.disabled = true;
            incBtn.classList.remove('btn-success');
            incBtn.classList.add('btn-secondary');
        } else {
            incBtn.disabled = false;
            incBtn.classList.remove('btn-secondary');
            incBtn.classList.add('btn-success');
        }

        if (quantity === 0) {
            card.remove();

            if (
                document.querySelectorAll('.quantity-control')
                    .length === 0
            ) {
                location.reload();
            }
        }
    }

    decBtn.addEventListener('click', async () => {

        const currentQty = parseInt(input.value);

        if (currentQty <= 1) {

            const result =
                await updateCartQuantity(thingId, 0);

            if (result.success) {

                await updateDisplay(
                    0,
                    0,
                    result.cart_total,
                    result.cart_count,
                    result.stock
                );
            }

        } else {

            const newQty = currentQty - 1;

            const result =
                await updateCartQuantity(
                    thingId,
                    newQty
                );

            if (result.success) {

                const newSubtotal =
                    newQty * pricePerItem;

                await updateDisplay(
                    newQty,
                    newSubtotal,
                    result.cart_total,
                    result.cart_count,
                    result.stock
                );
            }
        }
    });

    incBtn.addEventListener('click', async () => {

        if (incBtn.disabled) return;

        const currentQty =
            parseInt(input.value);

        const newQty =
            currentQty + 1;

        const result =
            await updateCartQuantity(
                thingId,
                newQty
            );

        if (result.success) {

            const newSubtotal =
                newQty * pricePerItem;

            await updateDisplay(
                newQty,
                newSubtotal,
                result.cart_total,
                result.cart_count,
                result.stock
            );

        } else if (result.max_reached) {

            incBtn.disabled = true;

            incBtn.classList.remove(
                'btn-success'
            );

            incBtn.classList.add(
                'btn-secondary'
            );

            incBtn.textContent =
                'Больше нет!';

            setTimeout(() => {
                incBtn.textContent = '+';
            }, 1500);
        }
    });
});

const totalPriceElement =
    document.getElementById('total-price');

if (totalPriceElement) {

    const initialTotal =
        parseInt(totalPriceElement.textContent);

    checkBalance(initialTotal);
}

fetch('/shop/cart-count/')
    .then(response => response.json())
    .then(data => {
        updateCartCount(data.cart_count);
    })
    .catch(error => {
        console.error(error);
    });
