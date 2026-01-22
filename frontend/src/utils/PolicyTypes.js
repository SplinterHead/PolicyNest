export const PolicyTypes = {
  Buildings: {
    colour: 'blue-grey-darken-2',
    icon: 'mdi-home-city',
    label: 'Buildings',
  },
  Car: {
    colour: 'blue-darken-2',
    icon: 'mdi-car',
    label: 'Car',
  },
  Contents: {
    colour: 'amber-darken-3',
    icon: 'mdi-sofa',
    label: 'Contents',
  },
  Life: {
    colour: 'purple-darken-2',
    icon: 'mdi-heart-pulse',
    label: 'Life',
  },
  Medical: {
    colour: 'teal-darken-2',
    icon: 'mdi-medical-bag',
    label: 'Medical',
  },
  Pet: {
    colour: 'brown-darken-1',
    icon: 'mdi-paw',
    label: 'Pet',
  },
}

export const getPolicyColour = (type) => {
  return PolicyTypes[type]?.colour
}

export const getPolicyIcon = (type) => {
  return PolicyTypes[type]?.icon
}
