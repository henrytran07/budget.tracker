function colorCard(expense, income, balance) {
    let expenseCard;
    let incomeCard;
    let balanceCard;

    if (income <= 0 || expense > income) {
        expenseCard = "red";
        incomeCard = "red";
        balanceCard = "red";
    } else if (expense >= income * 0.75) {
        expenseCard = "yellow";
        incomeCard = "yellow";
        balanceCard = "yellow";
    } else {
        expenseCard = "green";
        incomeCard = "green";
        balanceCard = "green";
    }

    return {expenseCard, incomeCard, balanceCard};
}

export default colorCard; 