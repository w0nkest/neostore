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

document.querySelectorAll('.view-cert').forEach(btn => {
    btn.addEventListener('click', function () {
        document.getElementById('view-cert-name').textContent = this.dataset.name;
        document.getElementById('view-cert-givenfor').textContent = this.dataset.givenfor;
        document.getElementById('view-cert-date').textContent = this.dataset.date;
        document.getElementById('view-cert-status').textContent = this.dataset.state;

        const photoDiv = document.getElementById('view-cert-photo');
        const photoUrl = this.dataset.photo;

        if (photoUrl) {
            if (photoUrl.endsWith('.pdf')) {
                photoDiv.innerHTML =
                    `<a href="${photoUrl}" target="_blank" class="btn btn-primary">Открыть PDF</a>`;
            } else {
                photoDiv.innerHTML =
                    `<a href="${photoUrl}" target="_blank">
                        <img src="${photoUrl}" class="img-thumbnail" style="max-width:150px;cursor:pointer;">
                    </a>
                    <small class="d-block text-muted mt-1">Нажмите для увеличения</small>`;
            }
        } else {
            photoDiv.innerHTML =
                '<span class="text-muted">Нет файла</span>';
        }

        const modal = new bootstrap.Modal(
            document.getElementById('certModal')
        );

        modal.show();
    });
});

document.querySelectorAll('.delete-cert').forEach(btn => {
    btn.addEventListener('click', function () {

        if (!confirm('Вы уверены, что хотите удалить этот сертификат?')) {
            return;
        }

        const certId = this.dataset.id;

        fetch(`/delete-cert/${certId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(
                        'Ошибка: ' +
                        (data.error || 'Что-то пошло не так')
                    );
                }
            })
            .catch(error => {
                console.error(error);
                alert('Не удалось удалить сертификат');
            });
    });
});