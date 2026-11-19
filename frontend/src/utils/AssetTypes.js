export const AssetTypes = {
  Vehicle: {
    colour: 'blue-darken-2',
    darkColour: 'blue-lighten-2',
    icon: 'mdi-car',
    label: 'Vehicle',
  },
  Pet: {
    colour: 'brown-darken-1',
    darkColour: 'brown-lighten-3',
    icon: 'mdi-paw',
    label: 'Pet',
  },
}

export const getAssetColour = (type, isDark = false) => {
  return (
    (isDark ? AssetTypes[type]?.darkColour : AssetTypes[type]?.colour) || AssetTypes[type]?.colour
  )
}

export const getAssetIcon = (type) => {
  return AssetTypes[type]?.icon
}
