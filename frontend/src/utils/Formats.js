export const currencyFormat = (value) => {
  if (value === undefined || value === null) return 'N/A'

  const currencyCode = localStorage.getItem('currencyCode')
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: currencyCode,
    currencyDisplay: 'narrowSymbol',
  }).format(value)
}
