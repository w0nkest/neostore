const checkboxes = document.querySelectorAll('.user-checkbox');
const selectAll = document.getElementById('select-all');
const rewardBtn = document.getElementById('reward-btn');
const rewardAmount = document.getElementById('reward-amount');
const form = document.getElementById('reward-form');
const selectedUsersInput = document.getElementById('selected-users');
const formAmount = document.getElementById('form-amount');

function updateRewardButton() {
    const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
    const amountValid = rewardAmount.value && parseInt(rewardAmount.value) > 0;
    rewardBtn.disabled = !(anyChecked && amountValid);
}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateRewardButton);
});

rewardAmount.addEventListener('input', updateRewardButton);

selectAll.addEventListener('change', function () {
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
    updateRewardButton();
});

rewardBtn.addEventListener('click', function (e) {
    e.preventDefault();

    const selectedUsers = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    if (selectedUsers.length === 0) {
        alert('Пожалуйста, выберите хотя бы одного пользователя');
        return;
    }

    const amount = parseInt(rewardAmount.value);

    if (!amount || amount <= 0) {
        alert('Пожалуйста, введите корректную сумму');
        return;
    }

    selectedUsersInput.value = JSON.stringify(selectedUsers);
    formAmount.value = amount;
    form.submit();
});