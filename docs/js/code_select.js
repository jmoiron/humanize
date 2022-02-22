/**
 * Disable user selection for '>>>' nodes inside code blocks.
 */
function disablePyConsolePromptsUserSelection() {
    const spans = document.getElementsByClassName('o');
    for (let i=0; i<spans.length; i++) {
        const span = spans[i];
        if (span.innerText === '>>>') {
            // if the next is a text node with a space as content
            // move the space to the span so it will not be selectable
            if (span.nextSibling.data === ' ') {
                span.innerText = '>>> '
                span.nextSibling.data = ''
            }
            span.classList.add('no-user-select');
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    disablePyConsolePromptsUserSelection();
})
