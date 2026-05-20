document.querySelectorAll(".toggle-password").forEach((button) => {
  button.addEventListener("click", () => {
    const input = button.closest(".input-group").querySelector(".password-field");
    const icon = button.querySelector("i");
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    icon.className = show ? "bi bi-eye-slash" : "bi bi-eye";
    button.setAttribute("aria-label", show ? "Hide password" : "Show password");
  });
});