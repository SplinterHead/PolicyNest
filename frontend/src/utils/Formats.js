export const currencyFormat = (value, code) => {
  if (value === undefined || value === null || value === '') return 'N/A'

  let currencyCode = code
  if (!currencyCode) {
    try {
      currencyCode = localStorage.getItem('currencyCode')
    } catch {
      currencyCode = null
    }
  }

  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: currencyCode || 'GBP',
    currencyDisplay: 'narrowSymbol',
  }).format(value)
}

export const parseIsoDate = (isoStr) => {
  if (!isoStr) return null
  if (isoStr instanceof Date) return isoStr

  const match = String(isoStr).match(/^(\d{4})-(\d{2})-(\d{2})/)
  if (match) {
    const [, year, month, day] = match
    return new Date(Number(year), Number(month) - 1, Number(day))
  }

  const parsed = new Date(isoStr)
  return Number.isNaN(parsed.getTime()) ? null : parsed
}

export const toIsoDate = (value) => {
  if (!value) return null
  if (typeof value === 'string') {
    const match = value.match(/^(\d{4}-\d{2}-\d{2})/)
    if (match) return match[1]
  }

  const date = value instanceof Date ? value : parseIsoDate(value)
  if (!date || Number.isNaN(date.getTime())) return null

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export const formatDate = (isoStr, emptyLabel = '') => {
  const date = parseIsoDate(isoStr)
  if (!date) return emptyLabel
  return date.toLocaleDateString()
}
