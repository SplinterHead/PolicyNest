export const POLICY_THEME = {
  Buildings: {
    colour: 'blue-grey-darken-2',
    icon: 'mdi-home-city',
    label: 'Buildings Insurance',
  },
  Car: {
    colour: 'blue-darken-2',
    icon: 'mdi-car',
    label: 'Vehicle Insurance',
  },
  Contents: {
    colour: 'amber-darken-3',
    icon: 'mdi-sofa',
    label: 'Contents Insurance',
  },
  Life: {
    colour: 'purple-darken-2',
    icon: 'mdi-heart-pulse',
    label: 'Life Insurance',
  },
  Medical: {
    colour: 'teal-darken-2',
    icon: 'mdi-medical-bag',
    label: 'Health Insurance',
  },
  Pet: {
    colour: 'brown-darken-1',
    icon: 'mdi-paw',
    label: 'Pet Insurance',
  },
  Other: {
    colour: 'grey-darken-2',
    icon: 'mdi-file-certificate',
    label: 'Other Policy',
  },
}

export const getPolicyColour = (type) => {
  return POLICY_THEME[type]?.colour || POLICY_THEME['Other'].colour
}

export const getPolicyIcon = (type) => {
  return POLICY_THEME[type]?.icon || POLICY_THEME['Other'].icon
}
