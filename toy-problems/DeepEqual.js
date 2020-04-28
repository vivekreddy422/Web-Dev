function deepEqual(obj1, obj2) {
    if(obj1 === null && obj2 === null) {
        return true;
    }
    if(typeof(obj1) === typeof(obj2)) {
        if(obj1 != null && obj2 != null) {
            if (typeof(obj1) != "object" && typeof(obj2) != "object") {
                if(obj1 === obj2) {
                    return true;
                } else {
                    return false
                }
            } else {
                let keys1 = Object.keys(obj1)
                let keys2 = Object.keys(obj2)
                if (keys1.length != keys2.length) {
                    return false
                } else {
                    let count = 0;
                    for (let i = 0; i < keys1.length; i++) {
                        for (let j = 0; j < keys2.length; j++) {
                            if (typeof(keys1[i]) === typeof(keys2[j])) {
                                if (typeof(obj1[keys1[i]]) !== "object" && typeof(obj2[keys2[j]]) !== "object") {
                                    if (obj1[keys1[i]] === obj2[keys2[j]]) {
                                        count++
                                        break;
                                    }
                                } else {
                                    if (deepEqual(obj1[keys1[i]], obj2[keys2[j]])) {
                                        count++
                                    }
                                } 
                            }
                        }
                    }
                    if (count === keys1.length) {
                        return true
                    } else {
                        return false
                    }
                }
            }
        } else {
            return false
        }
    } else {
        return false
    }
    
}

obj1 = {a:1, b:{1:2, 3:4}, c:3}
obj2 = {b:{1:2, 3:4}, a:1, c:3 }
if (deepEqual(obj1, obj2)) {
    console.log("true")
} else {
    console.log("false")
}