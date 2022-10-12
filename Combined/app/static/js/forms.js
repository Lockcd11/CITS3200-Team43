let scopusAPIKeyForm = document.getElementById('scopusAPIKeyForm');
let apiKeyBtn = document.getElementById('apiKeyBtn');

let addKeyBtn = document.getElementById('addKeyBtn');
let scopusIDForm = document.getElementById('scopusIDForm');


const apiFormSubmit = (e) => {
    e.preventDefault();

    if (scopusAPIKeyForm.value === "") {
        return;
    }

    //scopusAPIKeyForm.value //? Contains the API Key Value
}


const addFormSubmit = (e) => {
    e.preventDefault();

    if (scopusIDForm.value === "") {
        return;
    }

    //scopusIDForm.value //? Contains the Scopus ID wanting to add
}

apiKeyBtn.addEventListener('click', apiFormSubmit);
addKeyBtn.addEventListener('click', addFormSubmit);