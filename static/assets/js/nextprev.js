let number = 1

function moveQuestion(isNext){
    neutralize();


    if(isNext)  number += 1
    else  number -= 1

    if(number==1){
        document.getElementById('prev').classList.add('d-none')
        document.getElementById('prev').classList.remove('d-block')
    }

    else if(number==8){
        document.getElementById('next').classList.add('d-none')
        document.getElementById('next').classList.remove('d-block')
        document.getElementById('form-submit').classList.add('d-block')
        document.getElementById('form-submit').classList.remove('d-none')
    }

    else {
        document.getElementById('prev').classList.add('d-block')
        document.getElementById('prev').classList.remove('d-none')
        document.getElementById('next').classList.add('d-block')
        document.getElementById('next').classList.remove('d-none')
        document.getElementById('form-submit').classList.add('d-none')
        document.getElementById('form-submit').classList.remove('d-block')
    }

    document.getElementById(number).classList.add('d-block')
    document.getElementById(number).classList.remove('d-none')
}

function neutralize(){
    for(let i = 1; i < 9; i++){
        document.getElementById(i).classList.remove('d-block')
        document.getElementById(i).classList.add('d-none')
    }
}