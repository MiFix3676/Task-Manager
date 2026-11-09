    let myInput = document.querySelector('input[name = "task_name"]')
    let addForm = document.querySelector(".add-form")
    let myList = document.querySelector(".task-list")
    addForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(addForm);
        let text = formData.get("task_name");
        if (text === "") {
            return;
        }

        fetch(addForm.action, {
            method: "post",
            body: formData
        })
            .then(function (response) {
                return response.json()
            })
            .then(function (data) {
                let newLi = document.createElement("li")
        newLi.classList.add("task-pending")
        newLi.innerHTML = `<h3>${text}</h3>
<div>Приоритет: Обычный <b>(Не выполнено)</b></div>
<div class="card-action">

<form class="toggle-form" action="/toggle" method="post" >
        <input type="hidden" name="task_id" value="${data.id}">
        <button class="btn-toggle btn-do" type="submit">
            Выполнить
        </button>
        </form>

<form class="delete-form" action="/delete" method="post">
        <input type="hidden" name="task_id" value="${data.id}">
        <button class="btn-delete" type="submit">Удалить</button>
    </form>
</div>`
                myList.appendChild(newLi)
                myInput.value = ""
            })
    })
    myList.addEventListener('click', function (event) {
        if (event.target.classList.contains("btn-delete")) {
            event.preventDefault()
            const deletes = event.target.closest('form')
            const taskCard = event.target.closest('li')
            fetch(deletes.action, {
                method: 'post',
                body: new FormData (deletes)
            })

                .then(function (response) {
                    taskCard.remove()
                    return response.json()
                })

                .then( function (data) {
                    console.log(data)
                })
        } else if (event.target.classList.contains('btn-toggle')) {
            event.preventDefault()
            const toggle = event.target.closest('form')
            const cardTask = event.target.closest('li')
            fetch(toggle.action, {
                method: 'post',
                body: new FormData (toggle)
            })

                .then(function (_response) {
                    let button = cardTask.querySelector('.btn-toggle')
                    let text = cardTask.querySelector('b')
                    button.classList.toggle('btn-do')
                    button.classList.toggle('btn-undo')
                    cardTask.classList.toggle('task-done')
                    cardTask.classList.toggle('task-pending')
                    if (button.innerText === 'Выполнить') {
                        button.innerText = 'Отменить'
                    } else if (button.innerText === 'Отменить') {
                        button.innerText = 'Выполнить'
                    }
                    if (text.innerText === '(Выполнено)') {
                        text.innerText = '(Не выполнено)'
                    } else if (text.innerText === '(Не выполнено)') {
                        text.innerText = '(Выполнено)'
                    }
                })
        }
    })