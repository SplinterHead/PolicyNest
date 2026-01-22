export const AssetTypes = {
  Vehicle: {
    colour: 'blue-darken-2',
    icon: 'mdi-car',
    label: 'Vehicle',
  },
}

export const getAssetColour = (type) => {
  return AssetTypes[type]?.colour
}

export const getAssetIcon = (type) => {
  return AssetTypes[type]?.icon
}
