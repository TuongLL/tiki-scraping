const fs = require("fs");
const { parse } = require("csv-parse");
const { stringify } = require("csv-stringify");
const { default: axios } = require("axios");
const headers = {
  "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
  Accept: "application/json, text/plain, */*",
  "Accept-Language": "en-US,en;q=0.9",
  "x-guess-token": "XQ2JPlVw3ym9rATW6OERKZNevzIBqYds",
  Connection: "keep-alive",
  TE: "Trailers",
};

const params = {
  platform: "web",
  version: "3",
};

const crawlProducts = async () => {
  //   const columns = [
  //     "id",
  //     "sku",
  //     "name",
  //     "url_key",
  //     "url_path",
  //     "type",
  //     "author_name",
  //     "book_cover",
  //     "brand_name",
  //     "short_description",
  //     "price",
  //     "list_price",
  //     "badges",
  //     "badges_new",
  //     "discount",
  //     "discount_rate",
  //     "rating_average",
  //     "review_count",
  //     "order_count",
  //     "favourite_count",
  //     "thumbnail_url",
  //     "thumbnail_width",
  //     "thumbnail_height",
  //     "freegift_items",
  //     "has_ebook",
  //     "inventory_status",
  //     "is_visible",
  //     "productset_id",
  //     "productset_group_name",
  //     "seller",
  //     "is_flower",
  //     "is_gift_card",
  //     "inventory",
  //     "url_attendant_input_form",
  //     "option_color",
  //     "stock_item",
  //     "salable_type",
  //     "seller_product_id",
  //     "installment_info",
  //     "url_review",
  //     "bundle_deal",
  //     "quantity_sold",
  //     "tiki_live",
  //     "original_price",
  //     "shippable",
  //     "impression_info",
  //     "advertisement",
  //     "availability",
  //     "primary_category_path",
  //     "product_reco_score",
  //     "seller_id",
  //     "visible_impression_info",
  //   ];
  const columns = [
    "id",
    "master_id",
    "sku",
    "name",
    "url_key",
    "url_path",
    "short_url",
    "type",
    "book_cover",
    "short_description",
    "price",
    "list_price",
    "original_price",
    "badges",
    "badges_new",
    "discount",
    "discount_rate",
    "rating_average",
    "review_count",
    "review_text",
    "favourite_count",
    "thumbnail_url",
    "has_ebook",
    "inventory_status",
    "inventory_type",
    "productset_group_name",
    "is_fresh",
    "seller",
    "is_flower",
    "has_buynow",
    "is_gift_card",
    "salable_type",
    "data_version",
    "day_ago_created",
    "all_time_quantity_sold",
    "meta_title",
    "meta_description",
    "meta_keywords",
    "is_baby_milk",
    "is_acoholic_drink",
    "description",
    "images",
    "warranty_policy",
    "brand",
    "current_seller",
    "other_sellers",
    "specifications",
    "product_links",
    "gift_item_title",
    "configurable_options",
    "configurable_products",
    "services_and_promotions",
    "promitions",
    "stock_item",
    "quantity_sold",
    "categories",
    "breadcrumbs",
    "installment_info_v2",
    "installment_info_v3",
    "is_seller_in_chat_whitelist",
    "inventory",
    "warranty_info",
    "return_and_exchange_policy",
    "is_tier_pricing_available",
    "is_tier_pricing_eligible",
    "benefits",
  ];
  const csvFile = "amply-23462.csv";
  const filename = `./products/${csvFile}`;
  const writableStream = fs.createWriteStream(filename);
  const stringifier = stringify({ header: true, columns: columns });
  const stream = fs
    .createReadStream(`../dataRaw/${csvFile}`)
    .pipe(parse({ delimiter: ",", from_line: 2, to_line: 102 }))
    .on("data", async function (row) {
      const product = {
        product_id: row[1],
        spid: row[38],
      };
      try {
        stream.pause();
        const { data } = await axios.get(
          `https://tiki.vn/api/v2/products/${product.product_id}`,
          {
            headers,
            params: { ...params, spid: product.spid },
          }
        );

        stringifier.write(data);
        stringifier.pipe(writableStream);

        console.log(JSON.stringify(data));
      } finally {
        stream.resume();
      }
    })
    .on("end", () => {
      console.log("CSV file successfully processed");
    });
};

crawlProducts();
