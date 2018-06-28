export const remove = (arr, item) => {
    var index = arr.indexOf(item);
    if (index !== -1) {
        arr.splice(index, 1);
    }
}
