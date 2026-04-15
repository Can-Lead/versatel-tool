window.PRODUCT_CATALOG = {
  meta: {
    version: "1.1.0",
    currency: "EUR",
    source: "CAN Lead Produktkatalog",
    pricingModel: {
      listPriceSource: "variant_and_term",
      discountEngine: {
        enabled: true,
        stackingStrategy: "priority_then_combinable",
        defaultPdfVisibility: false,
        supportedTargets: ["monthly", "connection", "hardware", "sla", "voice"],
        supportedModes: ["percent", "fixed", "override", "waive"]
      }
    }
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
          pricingRules: {
            allowDiscounts: true,
            discountableTargets: {
              monthly: true,
              connection: true,
              hardware: true,
              sla: false,
              voice: false
            },
            approvalRequiredBelowMargin: false,
            minMarginPercent: null
          },
          discounts: [
            {
              key: "connect_waived_connection_standard",
              internalName: "Connect Anschluss erlassen",
              scope: "product",
              targets: ["connection"],
              mode: "waive",
              value: null,
              priority: 100,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Anschlusskosten erlassen",
              validTerms: [36, 48, 60],
              validVariantKeys: ["300_100", "600_200", "1000_300"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            },
            {
              key: "connect_monthly_campaign_300_100",
              internalName: "Connect Aktionspreis 300/100",
              scope: "variant",
              targets: ["monthly"],
              mode: "fixed",
              value: 20.00,
              priority: 200,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Aktionspreis",
              validTerms: [36],
              validVariantKeys: ["300_100"],
              validAvailabilityStatuses: ["onnet", "buildings_passed", "nearnet"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            }
          ],
          variants: [
            {
              key: "300_100",
              label: "300 / 100 Mbit/s",
              bandwidthLabel: "300 Mbit/s",
              downloadMbit: 300,
              uploadMbit: 100,
              pricing: {
                list: {
                  monthly: 299.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: null,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 299.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 299.00,
                  listMonthlyPrice: 299.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard", "connect_monthly_campaign_300_100"]
                },
                {
                  months: 48,
                  monthlyPrice: 299.00,
                  listMonthlyPrice: 299.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                },
                {
                  months: 60,
                  monthlyPrice: 299.00,
                  listMonthlyPrice: 299.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                }
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
              pricing: {
                list: {
                  monthly: 449.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: null,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 449.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 449.00,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                },
                {
                  months: 48,
                  monthlyPrice: 449.00,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                },
                {
                  months: 60,
                  monthlyPrice: 449.00,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                }
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
              pricing: {
                list: {
                  monthly: 619.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: null,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 619.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 619.00,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                },
                {
                  months: 48,
                  monthlyPrice: 619.00,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                },
                {
                  months: 60,
                  monthlyPrice: 619.00,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["connect_waived_connection_standard"]
                }
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
          pricingRules: {
            allowDiscounts: true,
            discountableTargets: {
              monthly: true,
              connection: true,
              hardware: true,
              sla: false,
              voice: false
            },
            approvalRequiredBelowMargin: true,
            minMarginPercent: 10
          },
          discounts: [
            {
              key: "premium_monthly_campaign_300_300",
              internalName: "Premium Aktionspreis 300/300",
              scope: "variant",
              targets: ["monthly"],
              mode: "fixed",
              value: 50.00,
              priority: 200,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Aktionspreis",
              validTerms: [36],
              validVariantKeys: ["300_300"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            },
            {
              key: "premium_connection_discount_all",
              internalName: "Premium Anschlussrabatt Standard",
              scope: "product",
              targets: ["connection"],
              mode: "fixed",
              value: 500.00,
              priority: 100,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Sonderkondition Anschluss",
              validTerms: [36, 48, 60],
              validVariantKeys: ["300_300", "600_600", "1000_1000", "2000_2000", "5000_5000", "10000_10000"],
              validAvailabilityStatuses: ["onnet", "buildings_passed", "nearnet"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            },
            {
              key: "premium_special_bid_1000_1000",
              internalName: "Premium Sonderfreigabe 1000/1000",
              scope: "variant",
              targets: ["monthly", "hardware"],
              mode: "fixed",
              value: 75.00,
              priority: 300,
              combinable: false,
              showInPdf: false,
              pdfLabel: null,
              validTerms: [36, 48],
              validVariantKeys: ["1000_1000"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: true,
              minMarginPercent: 12
            }
          ],
          variants: [
            {
              key: "300_300",
              label: "300 / 300 Mbit/s",
              bandwidthLabel: "300 Mbit/s",
              downloadMbit: 300,
              uploadMbit: 300,
              pricing: {
                list: {
                  monthly: 449.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: 449.00,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 399.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 399.00,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_monthly_campaign_300_300", "premium_connection_discount_all"]
                },
                {
                  months: 48,
                  monthlyPrice: 381.65,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                },
                {
                  months: 60,
                  monthlyPrice: 359.20,
                  listMonthlyPrice: 449.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                }
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
              pricing: {
                list: {
                  monthly: 619.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: 619.00,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 559.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 559.00,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                },
                {
                  months: 48,
                  monthlyPrice: 526.15,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                },
                {
                  months: 60,
                  monthlyPrice: 495.20,
                  listMonthlyPrice: 619.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                }
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
              pricing: {
                list: {
                  monthly: 749.00,
                  connection: 1500.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: 749.00,
                  oldConnectionPrice: 1500.00,
                  oldHardwarePrice: null
                }
              },
              monthlyPrice: 669.00,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                {
                  months: 36,
                  monthlyPrice: 669.00,
                  listMonthlyPrice: 749.00,
                  connectionPrice: 1500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all", "premium_special_bid_1000_1000"]
                },
                {
                  months: 48,
                  monthlyPrice: 636.65,
                  listMonthlyPrice: 749.00,
                  connectionPrice: 500.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all", "premium_special_bid_1000_1000"]
                },
                {
                  months: 60,
                  monthlyPrice: 599.20,
                  listMonthlyPrice: 749.00,
                  connectionPrice: 0.00,
                  hardwarePriceOnce: 149.00,
                  applicableDiscountKeys: ["premium_connection_discount_all"]
                }
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
              monthlyPrice: 1234.05,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 1234.05, listMonthlyPrice: 1299.00, connectionPrice: 1500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 48, monthlyPrice: 1169.10, listMonthlyPrice: 1299.00, connectionPrice: 500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 60, monthlyPrice: 1136.63, listMonthlyPrice: 1299.00, connectionPrice: 0.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] }
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
              monthlyPrice: 1899.05,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 1899.05, listMonthlyPrice: 1999.00, connectionPrice: 1500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 48, monthlyPrice: 1799.10, listMonthlyPrice: 1999.00, connectionPrice: 500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 60, monthlyPrice: 1749.13, listMonthlyPrice: 1999.00, connectionPrice: 0.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] }
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
              monthlyPrice: 2469.05,
              connectionPrice: 1500.00,
              hardwarePriceOnce: 149.00,
              terms: [
                { months: 36, monthlyPrice: 2469.05, listMonthlyPrice: 2599.00, connectionPrice: 1500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 48, monthlyPrice: 2339.10, listMonthlyPrice: 2599.00, connectionPrice: 500.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] },
                { months: 60, monthlyPrice: 2274.13, listMonthlyPrice: 2599.00, connectionPrice: 0.00, hardwarePriceOnce: 149.00, applicableDiscountKeys: ["premium_connection_discount_all"] }
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
          ]
        },

        glasfaser_business_pro: {
          key: "glasfaser_business_pro",
          label: "1&1 Glasfaser Business Pro",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed", "nearnet", "offnet", "telekom_vorleistung", "unklar"]
          },
          pricingRules: {
            allowDiscounts: true,
            discountableTargets: {
              monthly: true,
              connection: true,
              hardware: true,
              sla: false,
              voice: false
            },
            approvalRequiredBelowMargin: true,
            minMarginPercent: 12
          },
          discounts: [
            {
              key: "business_pro_monthly_discount_entry",
              internalName: "Business Pro Einstiegskondition",
              scope: "variant",
              targets: ["monthly"],
              mode: "percent",
              value: 10,
              priority: 150,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Sonderkondition",
              validTerms: [36],
              validVariantKeys: ["50_10", "100_20", "200_50"],
              validAvailabilityStatuses: ["onnet", "buildings_passed", "nearnet"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            },
            {
              key: "business_pro_hardware_free",
              internalName: "Business Pro Hardware erlassen",
              scope: "product",
              targets: ["hardware"],
              mode: "waive",
              value: null,
              priority: 100,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Hardwarekosten erlassen",
              validTerms: [36, 48, 60],
              validVariantKeys: ["50_10", "100_20", "200_50", "500_100", "1000_200"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            }
          ],
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

        office_fast_secure: {
          key: "office_fast_secure",
          label: "1&1 Office Fast & Secure",
          availability: {
            allowedStatuses: ["onnet", "buildings_passed"],
            note: "Nur für Onnet und Buildings Passed"
          },
          pricingRules: {
            allowDiscounts: true,
            discountableTargets: {
              monthly: true,
              connection: true,
              hardware: true,
              sla: false,
              voice: false
            },
            approvalRequiredBelowMargin: false,
            minMarginPercent: null
          },
          discounts: [
            {
              key: "office_fast_secure_wechslerbonus",
              internalName: "Wechslerbonus",
              scope: "product",
              targets: ["monthly"],
              mode: "override",
              value: null,
              priority: 300,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Aktionspreis",
              validTerms: [24, 36],
              validVariantKeys: ["150_50", "300_100", "600_200", "1000_300"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            },
            {
              key: "office_fast_secure_hardware_free",
              internalName: "Hardware erlassen",
              scope: "product",
              targets: ["hardware"],
              mode: "waive",
              value: null,
              priority: 100,
              combinable: false,
              showInPdf: true,
              pdfLabel: "Hardwarekosten erlassen",
              validTerms: [24, 36],
              validVariantKeys: ["150_50", "300_100", "600_200", "1000_300"],
              validAvailabilityStatuses: ["onnet", "buildings_passed"],
              startDate: null,
              endDate: null,
              approvalRequired: false,
              minMarginPercent: null
            }
          ],
          variants: [
            {
              key: "150_50",
              label: "150 / 50 Mbit/s",
              bandwidthLabel: "150 Mbit/s",
              downloadMbit: 150,
              uploadMbit: 50,
              pricing: {
                list: {
                  monthly: 59.99,
                  connection: 0.00,
                  hardware: 149.00
                },
                display: {
                  oldMonthlyPrice: 59.99,
                  oldConnectionPrice: null,
                  oldHardwarePrice: null
                }
              },
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
            },
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
            },
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
            },
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
