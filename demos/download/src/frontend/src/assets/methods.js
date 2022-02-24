export function getDiscountPrice(price, discount){
    if (discount) {
        return price - (price * (discount / 100));
    }
    return price;
}