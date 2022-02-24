
export const state = () => ({
  products: [
    {
      id: 1,
      title: 'CanonImageCLASS',
      description: 'products.syltherine.description',
      price: 440,
      image: require(`~/assets/img/CanonImageCLASS.png`),
      category: "categories.standard",
      discount: 20,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: true,
      }],
      size:[{
        item: "size.height",
        val: "37cm"
      },{
        item: "size.width",
        val: "39cm"
      },{
        item: "size.length",
        val: "36cm"
      },{
        item: "size.dpi",
        val: "600x600dpi"
      }],
      labels: ['discount'],
      adId: null
    },
     {
      id: 2,
       title: 'XeroxB310DNI',
      description: 'products.lolito.description',
      price:400,
       image: require(`~/assets/img/XeroxB310DNI.png`),
      category: "categories.luxury",
      discount: null,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: true
      }],
      size:[{
        item: "size.height",
        val: "22cm"
      },{
        item: "size.width",
        val: "37cm"
      },{
        item: "size.length",
        val: "36cm"
      },{
        item: "size.dpi",
        val: "600x600dpi"
      }],
      labels: ['new'],
      adId: null
    },
    {
      id: 3,
      title: 'Rolivetti d-ColorMF3023',
      description: 'products.respira.description',
      price: 1000,
      image: require(`~/assets/img/Rolivetti d-ColorMF3023.png`),
      category: "categories.minimalist",
      discount: 20,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: true
      }],
      size:[{
        item: "size.height",
        val: "61cm"
      },{
        item: "size.width",
        val: "47cm"
      },{
        item: "size.length",
        val: "55cm"
      },{
        item: "size.dpi",
        val: "600x600dpi"
      }],
      labels: ['new', 'discount'],
      adId: null
    },
    {
      id: 4,
      title: 'EpsonWorkForce7620',
      description: 'products.printo.description',
      price: 250,
      image: require(`~/assets/img/EpsonWorkForce7620.png`),
      category: "categories.modern",
      discount: null,
      isAdvertisment: true,
      props: [{
        item: "props.multiScan",
        val: true
      },{
        item: "size.dpi",
        val: "1200x1200dpi"
      }],
      labels: ['advertisement'],
      adId: "ad_1"
    },
    {
      id: 5,
      title: 'BrotherMFC',
      description: 'products.grifo.description',
      price: 300,
      image: require(`~/assets/img/BrotherMFC-L2710DW.png`),
      category: "categories.heavyDuty",
      discount: null,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: false
      }],
      size:[{
        item: "size.height",
        val: "31cm"
      },{
        item: "size.width",
        val: "41cm"
      },{
        item: "size.length",
        val: "39cm"
      },{
        item: "size.dpi",
        val: "1200x1200dpi"
      }],
      labels: [],
      adId: null
    },
    {
      id: 6,
      title: 'HPColorLaserJetMFP',
      description: 'products.muggo.description',
      price: 4500,
      image: require(`~/assets/img/HPColorLaserJetMFP.png`),
      category: "categories.big",
      discount: null,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: false
      }],
      size:[{
        item: "size.height",
        val: "50cm"
      },{
        item: "size.width",
        val: "39cm"
      },{
        item: "size.length",
        val: "53cm"
      },{
        item: "size.dpi",
        val: "600x600dpi"
      }],
      labels: [],
      adId: null
    },
    {
      id: 7,
      title: 'HPMFPM476dn',
      description: 'products.pingky.description',
      price: 700,
      image: require(`~/assets/img/HPMFPM476dn.png`),
      category: "categories.good",
      discount: 15,
      isAdvertisment: null,
      props: [{
        item: "props.multiScan",
        val: true
      }],
      size:[{
        item: "size.height",
        val: "48cm"
      },{
        item: "size.width",
        val: "42cm"
      },{
        item: "size.length",
        val: "50cm"
      },{
        item: "size.dpi",
        val: "600x600dpi"
      }],
      labels: ['discount'],
      adId: null
      },
    {
      id: 8,
      title: 'KyoceraTASKalfa3253ci',
      description: 'products.potty.description',
      price: 1500,
      image: require(`~/assets/img/KyoceraTASKalfa3253ci.png`),
      category: "categories.highTech",
      discount: null,
      isAdvertisment: true,
      props: [{
        item: "props.multiScan",
        val: true
      }],
      size:[{
        item: "size.height",
        val: "25cm"
      },{
        item: "size.width",
        val: "20cm"
      },{
        item: "size.length",
        val: "15cm"
      }],
      labels: ['advertisement'],
      adId: "ad_2"
    },
  ],
  footerItems: [
    {
      icon: 'bi-trophy',
      title: 'footer.highQuality.title',
      description: 'footer.highQuality.description'
    },
    {
      icon: 'bi-check-circle',
       title: 'footer.warranty.title',
      description: 'footer.warranty.description'
    },
    {
      icon: 'bi-box-seam',
       title: 'footer.shipping.title',
      description: 'footer.shipping.description'
    },
    {
      icon: 'bi-telephone-inbound',
      title: 'footer.support.title',
      description: 'footer.support.description'
    }
  ],
  userInfo: {
    hasSearched: false
  }
})

export const getters = {
  productsAdded: state => {
    return state.products.filter(el => {
      return el.isAddedToCart;
    });
  },
  getProductById: state => id => {
    return state.products.find(product => product.id == id);
  },
}

export const mutations = {
  setHasUserSearched: (state, hasSearched) => {
    state.userInfo.hasSearched = hasSearched;
  },
   setProductTitleSearched: (state, titleSearched) => {
    state.userInfo.productTitleSearched = titleSearched;
  },
}
