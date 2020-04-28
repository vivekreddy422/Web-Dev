function countBs(word) {
    return countChar(word, "B")
}

console.log(countBs("BigBoyToys"))

function countChar(word, letter) {
    let count = 0;
    for (let i = 0; i < word.length; i++) {
        if(word[i] === letter) {
            count++;
        }
    }
    return count;
}