window.onload = () => {

    const createAccountSection = document.querySelector('.create-account-section-link');
    const inputsContainer = document.querySelector('.sign-into-inputs');
    const h3 = document.querySelector('.sign-into-headers > h3');
    const userInput = document.querySelector('.sign-into-input-username > input');
    const rememberSection = document.querySelector('.sign-into-remember-me-section');
    
    // TRANSFORM PAGE TO SIGN UP
    createAccountSection.querySelector('#sign-in').onclick = () => {
        // CREATE AND APPEND INPUTS
    
        h3.style.animation = 'hide-h3 0.6s forwards ease-in';
        h3.innerText = 'Sign up to';
        h3.style.animation = 'show-h3 0.6s forwards ease-in';
    
        
        userInput.placeholder = 'Enter your user name';
        
        createInputs('sign-into-input-email', 'Email', 'email', 'Enter your email', inputsContainer, userInput.parentElement);
        createInputs('sign-into-input-confirm-password', 'Confirm Password', 'password', 'Confirm your password', inputsContainer);
    
        inputsContainer.querySelectorAll('div > label').forEach(elem => {
            elem.classList.add('before-active');
        })
    
        rememberSection.style.display = 'none';
    
        document.querySelector('.sign-into-send-login-info > #sign-into-button').style.display = 'none';
        document.querySelector('.sign-into-send-login-info > #create-account-button').style.display = 'block';
    
        createAccountSection.querySelector('p.sign-in').style.display = 'none';
        createAccountSection.querySelector('p.sign-up').style.display = 'block';
    }


    // TRANSFORM TO SIGN IN
    createAccountSection.querySelector('#sign-up').onclick = () => {
        document.querySelector('.sign-into-input-email').remove()
        document.querySelector('.sign-into-input-confirm-password').remove()

        userInput.placeholder = 'Enter your name or email';


        h3.style.animation = 'hide-h3 0.6s forwards ease-in';
        h3.innerText = 'Sign in to';
        h3.style.animation = 'show-h3 0.6s forwards ease-in';

        inputsContainer.querySelectorAll('div > label').forEach(elem => {
            elem.classList.remove('before-active');
        })

        rememberSection.style.display = 'flex';

        document.querySelector('.sign-into-send-login-info > #sign-into-button').style.display = 'block';
        document.querySelector('.sign-into-send-login-info > #create-account-button').style.display = 'none';
       

        createAccountSection.querySelector('p.sign-in').style.display = 'block';
        createAccountSection.querySelector('p.sign-up').style.display = 'none';

    }














    document.querySelector('#sign-into-button').onclick = () => {
        console.log('Login')
    }
    
    document.querySelector('#create-account-button').onclick = () => {
        console.log('Register')
    }



}    



    





function createInputs($el1, $label, $inputType,  placeholder, elemToAppend, childNode = null) {
    const div = document.createElement('div');
    const label = document.createElement('label');
    const input = document.createElement('input');

    div.classList.add($el1);

    div.style.opacity = 0;
    div.style.transition = 'all 0.3s ease-in';

    div.style.animation = 'show-email-div 0.3s forwards ease-in';

    label.innerText = $label;
    label.setAttribute('for', $inputType);


    input.type = $inputType;
    input.placeholder = placeholder
    input.name = $inputType;
    input.id = $inputType;

    div.append(label)
    div.append(input)

    if (childNode) {
        elemToAppend.insertBefore(div, childNode);
    } else {
        elemToAppend.append(div)
    }
}
