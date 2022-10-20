function isEmail(email) {
	const re =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	return re.test(String(email).toLowerCase())
}

function isEmpty(string) {
	return string.trim().length <= 0
}

function isNumber(num) {
	return Number.isInteger(parseInt(num))
}

function validateForm(input) {
	input.onblur = () => {
		if (isEmpty(input.value)) {
			input.classList.add("danger")
		}
		if (['day', 'month', 'year'].includes(input.name)) {
			if(!isNumber(input.value)) {
				input.classList.add('danger')
			}
		}
	}

	input.oninput = () => {
		if (input.classList.contains("danger")) {
			input.classList.remove("danger")
		}
	}
}

const formsInput = document.querySelectorAll('input[type="text"]')
const form = document.querySelector('#form')
console.log(form)
const signup = document.querySelector('#signup')
console.log(signup)

formsInput.forEach((input) => {
	validateForm(input)
})

form.onsubmit = (e) => {
	console.log("Submit")
	e.preventDefault()
}

// signup.onclick = () => {
// 	console.log(form.action)
// }