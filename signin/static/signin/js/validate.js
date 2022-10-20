const username = document.querySelector('input[name="username"]')
const password = document.querySelector('input[name="password"]')
const usernameMessage = username.nextElementSibling
const passwordMessage = password.nextElementSibling
const signinForm = document.querySelector('.form')

function checkTyped(str) {
	return str.trim().length > 0
}

function validateUsername() {
	if (!checkTyped(username.value)) {
		username.classList.add("danger")
		usernameMessage.classList.add("active")
		return false
	} else {
		username.classList.remove("danger")
		return true
	}
}

function validatePassword() {
	if (checkTyped(password.value)) {
		if (!validPassword(password.value)) {
			password.classList.add("danger")
			passwordMessage.innerText =
				"Password at least 8 chars, 1 uppercase and 1 number"
			passwordMessage.classList.add("active")
			return false
		}
		return true
	} else {
		password.classList.add("danger")
		passwordMessage.innerText = "Please enter your password"
		passwordMessage.classList.add("active")
		return false
	}
}

function validPassword(password) {
	// Minimum eight characters, at least one uppercase letter and one number
	const passwordRegex = new RegExp(
		/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$/
	)
	return passwordRegex.test(password.trim())
}

// Validate username
username.onblur = validateUsername

username.oninput = () => {
	if (username.classList.contains("danger")) {
		usernameMessage.classList.remove("active")
		username.classList.remove("danger")
	}
}

// Validate password
password.onblur = validatePassword

password.oninput = () => {
	if (password.classList.contains("danger")) {
		passwordMessage.classList.remove("active")
		password.classList.remove("danger")
	}
}

signinForm.onsubmit = (e) => {
	e.preventDefault()
	if (validatePassword() && validateUsername()) {
		console.log("Call API")
		// Call API
	}
}