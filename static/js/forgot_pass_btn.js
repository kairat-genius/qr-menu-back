const forgotPassword = document.querySelector('#sign-into-forgot-password');
const signIntoElement = document.querySelector('#sign');
const circle = document.getElementById('animated-circle-container');
const bigCircle = document.querySelector('.circle');

const mainColor = '#15C5CE';

forgotPassword.onclick = () => {
    const signIntoDiv = document.querySelector('.sign-into-container');
    signIntoDiv.remove();

    circle.classList.add('up');

    const div = document.createElement('div');
    div.classList.add('reset-password-container');

    const svgDiv = document.createElement('div');
    svgDiv.classList.add('svg-elem-container');
    svgDiv.style.margin = '2rem 0';
    svgDiv.style.display = 'flex';
    svgDiv.style.justifyContent = 'center';
    svgDiv.style.alignItems = 'center';

    svgDiv.innerHTML = 
        '<svg viewbox="0 0 55 55" width="55px" height="55px"><circle fill="#BDDDFF" cx="50%" cy="50%" r="25" /><circle id="tiny-circle" fill="#fff" cx="50%" cy="30%" r="3" /><line stroke="#fff" stroke-width="3.5px" stroke-linecap: round; x1="27.5px" y1="23px" x2="27.5px" y2="45px" /></svg>'


    const divHeader = document.createElement('div');
    divHeader.classList.add('reset-header-container');
    divHeader.style.textAlign = 'center';

    const h3 = document.createElement('h3');
    h3.style.fontFamily = '"Playfair Display", sans-serif'
    h3.style.fontSize = '2rem';
    h3.style.whiteSpace = 'nowrap';
    h3.innerText = 'Reset Password'
    
    divHeader.append(h3)

    const DivinfoAfterHeader = document.createElement('div');
    DivinfoAfterHeader.classList.add('reset-info-container');
    DivinfoAfterHeader.style.margin = '2rem 0';
    DivinfoAfterHeader.style.textAlign = 'center';

    const p = document.createElement('p');
    p.style.color = '#959895';
    p.style.lineHeight = '28px';
    p.innerText = 'Enter your email addres and we\'ll send you an email with instructions to reset your password';

    DivinfoAfterHeader.append(p);


    const resetInputDiv = document.createElement('div');
    resetInputDiv.style.margin = '2rem 0';
    resetInputDiv.style.display = 'flex';
    resetInputDiv.style.flexFlow = 'column nowrap';
    resetInputDiv.classList.add('reset-input-container')

    const resetLabel = document.createElement('label');
    resetLabel.setAttribute('for', 'email');
    resetLabel.style.width = 'min-content';
    resetLabel.style.margin = '0 0 2rem 0';
    resetLabel.innerText = 'Email';

    const resetInput = document.createElement('input');
    resetInput.style.padding = '0.8rem 1rem';
    resetInput.style.outline = 'none';
    resetInput.style.border = '1px solid #E1E1E1';
    resetInput.style.borderRadius = '5px';
    resetInput.placeholder = 'Enter your email';

    resetInput.onfocus = () => {resetInput.style.borderColor = mainColor}
    resetInput.onblur = () => {resetInput.style.borderColor = '#E1E1E1'}

    resetInputDiv.append(resetLabel);
    resetInputDiv.append(resetInput);

    const resetDivButton = document.createElement('div');
    resetDivButton.classList.add('reset-button-container');


    const resetButton = document.createElement('button');
    resetButton.style.width = '100%';
    resetButton.style.height = '3rem';
    resetButton.style.cursor = 'pointer';
    resetButton.style.border = 'none';
    resetButton.style.background = mainColor;
    resetButton.style.borderRadius = '5px';
    resetButton.style.color = '#fff';
    resetButton.style.transition = 'all 0.3s ease-in-out';
    resetButton.autofocus = true;
    resetButton.innerText = 'Reset';
    resetButton.onclick = resetPassword;

    resetDivButton.append(resetButton);


    signIntoElement.append(div);
    div.append(svgDiv);
    div.append(divHeader)
    div.append(DivinfoAfterHeader);
    div.append(resetInputDiv);
    div.append(resetDivButton);

    bigCircle.classList.add('move-x');



    const img1 = document.createElement('img');
    img1.src = '/static/images/forgot_pass/Frame 37294.png';
    img1.id = 'cfirst';
    
    const img2 = document.createElement('img');
    img2.src = '/static/images/forgot_pass/Frame 37298.png';
    img2.id = 'csecond';
    
    const img3 = document.createElement('img');
    img3.src = '/static/images/forgot_pass/Frame 37299.png';
    img3.id = 'cthird';

    const img4 = document.createElement('img');
    img4.src = '/static/images/forgot_pass/Frame 37301.png';
    img4.id = 'cfourth';

    bigCircle.append(img1);
    bigCircle.append(img2);
    bigCircle.append(img3);
    bigCircle.append(img4);

}

function resetPassword() {
    const emailDiv = document.querySelector('.reset-input-container');
    const email = emailDiv.querySelector('input').value;

    if (email.length > 4) {
        const svgDiv = document.querySelector('.svg-elem-container');
        svgDiv.querySelector('svg > circle').style.fill = '#C0E5D1';
        
        svgDiv.querySelector('svg > circle + circle').remove();
        svgDiv.querySelector('svg > line').remove();
    
        svgDiv.querySelector('svg').innerHTML = svgDiv.querySelector('svg').innerHTML + '<polyline fill="none" stroke="#fff" stroke-width="5px" points="16,29 25,37 38,17" stroke-dasharray="50" stroke-dashoffset="50" />'
    
    
        const h3 = document.querySelector('.reset-header-container > h3');
        h3.innerText = 'Succes !'
    
    
        const p = document.querySelector('.reset-info-container > p');
        p.innerText = `A email has been send to your ${email}. Please check for an email from company and click on the included link to reset your password`;
    
        emailDiv.remove();

        const button = document.querySelector('.reset-button-container > button');
        button.innerText = 'Back to home';
        button.onclick = () => {
            location.reload();
        }

    } else {
        const span = document.createElement('span');
        span.style.color = '#ff0000';
        span.innerText = 'Please enter your email before!'
        span.style.fontSize = '0.7rem'

        if (!emailDiv.querySelector('span')) {
            emailDiv.append(span);
        }

        emailDiv.querySelector('input').onfocus = () => {
            span.remove();
            emailDiv.querySelector('input').style.borderColor = mainColor;
        }
    }
}
