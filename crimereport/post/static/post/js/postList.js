const makeli = (response) => {
    return (
            "<li>" +
                    `<span class='reple-text'>${response.text}</span>`+
                    `<span class='reple-created'>${response.title}</span>`+
            `</li>`
    )
}

(async (post_id) => {
    const input_comment = await fetch(`http://127.0.0.1:8000/post/postlist/${post_id}/inputcomment/`, {
            method:'POST',
            headers:{
                'Accpet' : 'application/json',
                'Content-Type':'application/json'
            },
            credentials: 'same-origin',
            body: getdata,
        }).then(res => res.json())
        .then(response => document.querySelector('.detail-container ul').appendChild(makeli(response)) )
    
    const getdata = () => {
        const sendData = new Object();
        const loginform = document.commentform
        const comment_text = loginform.text.value
        sendData.text = comment_text
        sendData.post_id = post_id
        const jsonData = JSON.stringify(sendData)
        return jsonData
    }
})