window.PRODUCT_CATALOG = {
  meta: {
    version: "1.0.0",
    currency: "EUR",
    source: "CAN Lead Produktkatalog"
  },

  families: {
    internet: {
      key: "internet",
      label: "Internet",
      products: {
        glasfaser_connect: {
          key: "glasfaser_connect",
          label: "1&1 Glasfaser Connect",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed", "nearnet", "offnet", "telekom_vorleistung", "unklar"]
          },
          variants: [
            {
              key: "300_100",
              label: "300 / 100 Mbit/s",
              bandwidthLabel: "300 Mbit/s",
              downloadMbit: 300,
              uploadMbit: 100,
              monthlyPrice: 299.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 299.00 },
                { months: 48, monthlyPrice: 299.00 },
                { months: 60, monthlyPrice: 299.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "600_200",
              label: "600 / 200 Mbit/s",
              bandwidthLabel: "600 Mbit/s",
              downloadMbit: 600,
              uploadMbit: 200,
              monthlyPrice: 449.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 449.00 },
                { months: 48, monthlyPrice: 449.00 },
                { months: 60, monthlyPrice: 449.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "1000_300",
              label: "1000 / 300 Mbit/s",
              bandwidthLabel: "1000 Mbit/s",
              downloadMbit: 1000,
              uploadMbit: 300,
              monthlyPrice: 619.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 619.00 },
                { months: 48, monthlyPrice: 619.00 },
                { months: 60, monthlyPrice: 619.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            }
          ]
        },

        glasfaser_premium: {
          key: "glasfaser_premium",
          label: "1&1 Glasfaser Premium",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed", "nearnet", "offnet", "telekom_vorleistung", "unklar"]
          },
          variants: [
            {
              key: "300_300",
              label: "300 / 300 Mbit/s",
              bandwidthLabel: "300 Mbit/s",
              downloadMbit: 300,
              uploadMbit: 300,
              monthlyPrice: 449.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 449.00 },
                { months: 48, monthlyPrice: 449.00 },
                { months: 60, monthlyPrice: 449.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "600_600",
              label: "600 / 600 Mbit/s",
              bandwidthLabel: "600 Mbit/s",
              downloadMbit: 600,
              uploadMbit: 600,
              monthlyPrice: 619.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 619.00 },
                { months: 48, monthlyPrice: 619.00 },
                { months: 60, monthlyPrice: 619.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "1000_1000",
              label: "1000 / 1000 Mbit/s",
              bandwidthLabel: "1000 Mbit/s",
              downloadMbit: 1000,
              uploadMbit: 1000,
              monthlyPrice: 749.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 749.00 },
                { months: 48, monthlyPrice: 749.00 },
                { months: 60, monthlyPrice: 749.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "2000_2000",
              label: "2 / 2 Gbit/s",
              bandwidthLabel: "2 Gbit/s",
              downloadMbit: 2000,
              uploadMbit: 2000,
              monthlyPrice: 1299.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 1299.00 },
                { months: 48, monthlyPrice: 1299.00 },
                { months: 60, monthlyPrice: 1299.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "5000_5000",
              label: "5 / 5 Gbit/s",
              bandwidthLabel: "5 Gbit/s",
              downloadMbit: 5000,
              uploadMbit: 5000,
              monthlyPrice: 1999.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 1999.00 },
                { months: 48, monthlyPrice: 1999.00 },
                { months: 60, monthlyPrice: 1999.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "10000_10000",
              label: "10 / 10 Gbit/s",
              bandwidthLabel: "10 Gbit/s",
              downloadMbit: 10000,
              uploadMbit: 10000,
              monthlyPrice: 2599.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 2599.00 },
                { months: 48, monthlyPrice: 2599.00 },
                { months: 60, monthlyPrice: 2599.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            }
          ]
        },

        glasfaser_business_pro: {
          key: "glasfaser_business_pro",
          label: "1&1 Glasfaser Business Pro",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed", "nearnet", "offnet", "telekom_vorleistung", "unklar"]
          },
          variants: [
            {
              key: "50_10",
              label: "50 / 10 Mbit/s",
              bandwidthLabel: "50 Mbit/s",
              downloadMbit: 50,
              uploadMbit: 10,
              monthlyPrice: 399.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 399.00 },
                { months: 48, monthlyPrice: 399.00 },
                { months: 60, monthlyPrice: 399.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "100_20",
              label: "100 / 20 Mbit/s",
              bandwidthLabel: "100 Mbit/s",
              downloadMbit: 100,
              uploadMbit: 20,
              monthlyPrice: 499.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 499.00 },
                { months: 48, monthlyPrice: 499.00 },
                { months: 60, monthlyPrice: 499.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "200_50",
              label: "200 / 50 Mbit/s",
              bandwidthLabel: "200 Mbit/s",
              downloadMbit: 200,
              uploadMbit: 50,
              monthlyPrice: 599.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 599.00 },
                { months: 48, monthlyPrice: 599.00 },
                { months: 60, monthlyPrice: 599.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "500_100",
              label: "500 / 100 Mbit/s",
              bandwidthLabel: "500 Mbit/s",
              downloadMbit: 500,
              uploadMbit: 100,
              monthlyPrice: 699.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 699.00 },
                { months: 48, monthlyPrice: 699.00 },
                { months: 60, monthlyPrice: 699.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            },
            {
              key: "1000_200",
              label: "1000 / 200 Mbit/s",
              bandwidthLabel: "1000 Mbit/s",
              downloadMbit: 1000,
              uploadMbit: 200,
              monthlyPrice: 899.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 899.00 },
                { months: 48, monthlyPrice: 899.00 },
                { months: 60, monthlyPrice: 899.00 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true },
                { key: "plus", label: "Plus", priceMonthly: null, available: false },
                { key: "profi", label: "Profi", priceMonthly: null, available: false }
              ],
              voiceOptions: [
                { key: "sip_einzelanschluss", label: "SIP Einzelanschluss", priceMonthly: 0.00, available: true },
                { key: "sip_ddi", label: "SIP DDi Sprachkanäle", priceMonthly: 0.00, available: true }
              ]
            }
          ]
        },

        office_fast_secure_150: {
          key: "office_fast_secure_150",
          label: "1&1 Office Fast & Secure 150",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed"],
            note: "Nur für Onnet und Buildings Passed"
          },
          variants: [
            {
              key: "150_50",
              label: "150 / 50 Mbit/s",
              bandwidthLabel: "150 Mbit/s",
              downloadMbit: 150,
              uploadMbit: 50,
              monthlyPrice: 39.90,
              oldMonthlyPrice: 59.99,
              connectionPrice: 0.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 24, monthlyPrice: 39.90 },
                { months: 36, monthlyPrice: 39.90 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true }
              ],
              voiceOptions: [],
              marketingBadges: ["Wechslerbonus"]
            }
          ]
        },

        office_fast_secure_300: {
          key: "office_fast_secure_300",
          label: "1&1 Office Fast & Secure 300",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed"]
          },
          variants: [
            {
              key: "300_100",
              label: "300 / 100 Mbit/s",
              bandwidthLabel: "300 Mbit/s",
              downloadMbit: 300,
              uploadMbit: 100,
              monthlyPrice: 49.90,
              oldMonthlyPrice: 79.99,
              connectionPrice: 0.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 24, monthlyPrice: 49.90 },
                { months: 36, monthlyPrice: 49.90 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true }
              ],
              voiceOptions: [],
              marketingBadges: ["Wechslerbonus"]
            }
          ]
        },

        office_fast_secure_600: {
          key: "office_fast_secure_600",
          label: "1&1 Office Fast & Secure 600",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed"]
          },
          variants: [
            {
              key: "600_200",
              label: "600 / 200 Mbit/s",
              bandwidthLabel: "600 Mbit/s",
              downloadMbit: 600,
              uploadMbit: 200,
              monthlyPrice: 59.90,
              oldMonthlyPrice: 99.99,
              connectionPrice: 0.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 24, monthlyPrice: 59.90 },
                { months: 36, monthlyPrice: 59.90 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true }
              ],
              voiceOptions: [],
              marketingBadges: ["Wechslerbonus", "Bestseller"]
            }
          ]
        },

        office_fast_secure_1000: {
          key: "office_fast_secure_1000",
          label: "1&1 Office Fast & Secure 1000",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed"]
          },
          variants: [
            {
              key: "1000_300",
              label: "1000 / 300 Mbit/s",
              bandwidthLabel: "1000 Mbit/s",
              downloadMbit: 1000,
              uploadMbit: 300,
              monthlyPrice: 69.90,
              oldMonthlyPrice: 109.99,
              connectionPrice: 0.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 24, monthlyPrice: 69.90 },
                { months: 36, monthlyPrice: 69.90 }
              ],
              slaOptions: [
                { key: "basis", label: "Basis", priceMonthly: 0.00, available: true }
              ],
              voiceOptions: [],
              marketingBadges: ["Wechslerbonus"]
            }
          ]
        }
      }
    },

    managed_wlan: {
      key: "managed_wlan",
      label: "Managed WLAN",
      products: {}
    },

    unified_communications: {
      key: "unified_communications",
      label: "Unified Communications",
      products: {}
    }
  }
};
