<script>
import Title from './sections/Title.vue'
import Abstract from './sections/Abstract.vue'
import Markdown from './sections/Markdown.vue'
import BibTeX from './sections/BibTeX.vue'
import Carousel from './sections/Carousel.vue'
import Video from './sections/Video.vue'
import ImageSlider from './sections/ImageSlider.vue'
import ImageSliderInner from './sections/ImageSliderInner.vue'
import ImageSelector from './sections/ImageSelector.vue'
import Echart from './sections/Echart.vue'
import Table from './sections/Table.vue'
import Collapse from './sections/Collapse.vue'
import SeletionForComparison from './sections/SeletionForComparison.vue'
import Comment from './sections/Comment.vue'
import Latex from './sections/Latex.vue'
import Model3D from './sections/Model3D.vue'
import GaussianSplats3D from './sections/GaussianSplats3D.vue'
import PdfReader from './sections/PdfReader.vue'
import Curve from './sections/Curve.vue'
import InferReal from './sections/InferReal.vue'

export default {
  components: {
    Title,
    InferReal,
    Abstract,
    Markdown,
    BibTeX,
    Carousel,
    Video,
    ImageSlider,
    ImageSliderInner,
    ImageSelector,
    Echart,
    Collapse,
    Table,
    SeletionForComparison,
    Comment,
    Latex,
    Model3D,
    GaussianSplats3D,
    PdfReader,
    Curve,
    
  }
}
</script>

<template>
  <Title/>
  <!-- <Carousel/> -->
  <Video/>
  <InferReal/>
  <Abstract/>
  <Markdown/>
  <Latex/>
  <Table/>
  <!-- <Collapse/> -->
  <Echart/>
  <!-- <Model3D/> -->
  <!-- <GaussianSplats3D/> -->
  
  <SeletionForComparison/>
  <PdfReader/>
  <Curve/>
  <!-- <ImageSliderInner/> -->
  <!-- <ImageSlider/> -->
  <!-- <ImageSelector/> -->
  <BibTeX/>
  <!-- <Comment/> -->
</template>