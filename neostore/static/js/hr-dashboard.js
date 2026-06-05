let currentCertId = null;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.querySelectorAll('.mark-delivered').forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.dataset.id;
            const row = document.getElementById(`order-${orderId}`);

            fetch(`/mark-order/${orderId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.remove();
                    const ordersTable = document.getElementById('orders-table');
                    if (ordersTable.children.length === 0) {
                        ordersTable.innerHTML = '<tr id="no-orders"><td colspan="3">Нет ожидающих заказов.</td>';
                    }
                } else {
                    alert('Error: ' + (data.error || 'Something went wrong'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Не удалось отметить заказ как доставленный');
            });
        });
    });

    document.querySelectorAll('.view-cert').forEach(btn => {
        btn.addEventListener('click', function() {
            const certName = this.dataset.name;
            const certUser = this.dataset.user;
            const certGivenFor = this.dataset.givenfor;
            const certDate = this.dataset.date;
            const certPhoto = this.dataset.photo;
            const certState = this.dataset.state || 'Ожидает';

            document.getElementById('view-cert-name').textContent = certName;
            document.getElementById('view-cert-user').textContent = certUser;
            document.getElementById('view-cert-givenfor').textContent = certGivenFor;
            document.getElementById('view-cert-date').textContent = certDate;
            document.getElementById('view-cert-status').textContent = certState;

            const photoContainer = document.getElementById('view-cert-photo');
            if (certPhoto && certPhoto !== '') {
                if (certPhoto.endsWith('.pdf')) {
                    photoContainer.innerHTML = '<a href="' + certPhoto + '" target="_blank" class="btn btn-primary">Открыть PDF</a>';
                } else {
                    photoContainer.innerHTML = '<a href="' + certPhoto + '" target="_blank"><img src="' + certPhoto + '" alt="Certificate Photo" class="img-fluid rounded" style="max-height: 300px; width: auto; cursor: pointer;"></a><small class="d-block text-muted mt-1">Нажмите для увеличения</small>';
                }
            } else {
                photoContainer.innerHTML = '<p class="text-muted">Файл не загружен</p>';
            }

            const modal = new bootstrap.Modal(document.getElementById('viewCertModal'));
            modal.show();
        });
    });

    document.querySelectorAll('.approve-cert').forEach(btn => {
        btn.addEventListener('click', function() {
            currentCertId = this.dataset.id;
            document.getElementById('current-cert-id').value = currentCertId;
            document.getElementById('cert-price').value = '';

            const modal = new bootstrap.Modal(document.getElementById('priceModal'));
            modal.show();
        });
    });

    document.getElementById('confirm-approve').addEventListener('click', function() {
        const certId = document.getElementById('current-cert-id').value;
        const price = document.getElementById('cert-price').value;
        const row = document.getElementById(`cert-${certId}`);

        if (!price || parseInt(price) <= 0) {
            alert('Пожалуйста, введите корректную сумму награды');
            return;
        }

        fetch(`/approve-cert/${certId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reward: parseInt(price) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                row.remove();
                const certsTable = document.getElementById('certificates-table');
                if (certsTable.children.length === 0) {
                    certsTable.innerHTML = '<tr id="no-certs"><td colspan="3">Нет ожидающих сертификатов.<tr>';
                }
                const modal = bootstrap.Modal.getInstance(document.getElementById('priceModal'));
                modal.hide();
            } else {
                alert('Error: ' + (data.error || 'Something went wrong'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Не удалось одобрить сертификат');
        });
    });