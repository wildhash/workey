import Hero from '@/components/Hero';
import ProjectGrid from '@/components/ProjectGrid';
import Skills from '@/components/Skills';
import Contact from '@/components/Contact';
import Nav from '@/components/Nav';

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Nav />
      <Hero />
      <ProjectGrid />
      <Skills />
      <Contact />
    </main>
  );
}
