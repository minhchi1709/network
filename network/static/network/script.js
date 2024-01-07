document.addEventListener("DOMContentLoaded", () => {
    // Find all next button
    document.querySelectorAll('.next').forEach(button => {
        // If the next button is clicked, load the next page
        button.addEventListener('click', () => {
            const id = getId(button.id);
            document.getElementById(id).style.display = 'none';
            document.getElementById(id + 1).style.display = 'block';
        });
    });

    // Find all previous button
    document.querySelectorAll('.previous').forEach(button => {
        // If the previous button is clicked, load the next page
        button.addEventListener('click', () => {
            const id = getId(button.id);
            document.getElementById(id).style.display = 'none';
            document.getElementById(id - 1).style.display = 'block';
        });
    });

    // Find all edit button
    document.querySelectorAll('.edit').forEach(button => {
        
        button.addEventListener('click', () => {
            const id = getId(button.id);
            
            // Make the save button visible
            const save = document.getElementById(`${id}-save`);
            save.style.display = 'inline';
            // Enable changes
            const content = document.getElementById(`${id}-content`);
            const oldContent = content.innerHTML;
            let newContent = content.innerHTML;
            content.disabled = false;
            content.style.border = '1px solid black';
            
            console.log(newContent);
            // Record the changes
            content.addEventListener('input', event => {
                newContent = event.target.value;
            });
            // Wait until user confirm changes
            save.addEventListener('click', () => {
                // If the user leaves the content blank, give them an alert and restore the old content
                if (newContent === '') {
                    alert('Your content must not be blank!');
                    content.innerHTML = oldContent;
                } else {
                    // Otherwise update in database

                    fetch(`/edit/${id}`, {
                        method: "PUT",
                        body: JSON.stringify({
                            content: newContent
                        })
                    })
                }
                content.disabled = true;
                content.style.border = 'none';
                save.style.display = 'none';
            });
        });
    });

    // Find all like button
    document.querySelectorAll('.like').forEach(button => {
        // If the previous button is clicked, load the next page
        button.addEventListener('click', () => {
            const id = getId(button.id);
            const likes = document.getElementById(`${id}-likes`);
            
            // If user liked the post
            if (button.id === `${id}-like`) {
                // Update likes field
                likes.innerHTML = parseInt(likes.innerHTML) + 1;
                // Update the innerHTML and ID of the button to prevent us from liked or unliked a post more times
                document.getElementById(`${id}-like`).innerHTML = 'Unlike';
                document.getElementById(`${id}-like`).id = `${id}-unlike`; 
                // Update the database
                fetch(`/like/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        liked: true
                    })
                })
            } else if (button.id === `${id}-unlike`) {
                // Update likes field
                likes.innerHTML = parseInt(likes.innerHTML) - 1;
                // Update the innerHTML and ID of the button to prevent us from liked or unliked a post more times
                document.getElementById(`${id}-unlike`).innerHTML = 'Like';
                document.getElementById(`${id}-unlike`).id = `${id}-like`;
                // Update the database
                fetch(`/like/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        liked: false
                    })
                })
            }
        });
    });

    document.querySelectorAll('.comment').forEach(button => {
        button.addEventListener('click', () => {
            const id = getId(button.id);
            document.getElementById(`${id}-addcomment`).style.display = 'inline';
            button.style.display = 'none';
            const content = button.nextElementSibling.nextElementSibling;
            content.style.display = 'block';
            content.disabled = false;
            content.autofocus = true;
            content.required = true;
            let newContent = '';
            // Record the changes
            content.addEventListener('input', event => {
                newContent = event.target.value;
                console.log(newContent.length);
            });
            // Wait until user confirm changes
            document.getElementById(`${id}-addcomment`).addEventListener('click', () => {
                let blank = true;
                for (let i = 0 ; i < newContent.length ; i++) {
                    blank &= (newContent[i] === ' ');
                }
                console.log(blank);
                if (blank || newContent.length === 0) {
                    alert('Your comment can not be blank');
                }
                else {
                    document.getElementById(`${id}-addcomment`).style.display = 'none';
                    button.style.display = 'inline';
                    content.disabled = true;
                    content.readOnly = true;
                    fetch(`/comment/${id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            comment: newContent
                        })
                    })
                }
            });
        });
    });
    
});

// Parse the id 
function getId(str) {
    let id = '';
    for (let i = 0 ; i < str.length ; i++) {
        if (str[i] !== '-') {
            id += str[i];
        } else {
            return parseInt(id);
        }     
    }
    return id;
}