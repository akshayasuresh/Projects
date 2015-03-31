      program manual

      implicit real*8(a-h, o-z)
      double precision a,b,c,d,e,f,g,h,m1, m2, m3, m4,m5,m6,m7,m8
      parameter (nmax=201)
      dimension u11(1201,201),ub(201,201)
      common u(251,201)

      pi=4.0d0*atan(1.0d0)
      pb=3.83d0
      pm=6.39d0
      pw=12.0d0
      qm=pi
      dp=(pw-pm)/float(500)
      dq=qm/float(200)


42     format(4(f15.8,1x))
44     format(1(f15.8,1x))
      open (12, file='rtest.dat', status='unknown')
      open (13, file='thetatest.dat', status='unknown')
      open (14, file='corfieldtest.dat', status='unknown')
      write (*,*) 'A,B,C,D,E,F,G,H:'
      read (*,*) a,b,c,d,e,f,g,h
      do i=1,1001,4
        p=pm+dble(i-1)*dp
c        p=pm
c        write (12,44) p
        do j=1,201
          q=qm-dble(j-1)*dq
          if(i.eq.1) write (13,44) q
c          m1=a*(dsin(q)/(p**2))
c          m2=b*(3.0d0*dcos(q)*dsin(q)/(p**3))
c          m3=c*(1.5d0*(5.0d0*(dcos(q)**2)-1.0d0)*dsin(q)/(p**4))
c          m4=d*((5.d0/3.d0)*(7.d0*(dcos(q)**3)-3.d0*dcos(q)*dsin(q)))
c     &       /(p**5)
          x=dcos(q)
          m1=-1.d0*a*plgndr(1,1,x)/(p**2)
          m2=-1.d0*b*plgndr(2,1,x)/(p**3)
          m3=-1.d0*c*plgndr(3,1,x)/(p**4)
          m4=-1.d0*d*plgndr(4,1,x)/(p**5)
          m5=-1.d0*e*plgndr(5,1,x)/(p**6)
          m6=-1.d0*f*plgndr(6,1,x)/(p**7)
          m7=-1.d0*g*plgndr(7,1,x)/(p**8)
          m8=-1.d0*h*plgndr(8,1,x)/(p**9)
          cont=(m1+m2+m3+m4+m5+m6+m7+m8)*p*dsin(q)
c          write(14, 44) cont
        end do
      end do

      close(12)
      close(13)
      close(14)

      stop
      end


      function plgndr(l,m,x)
      implicit real*8(a-h,o-z)
      if(m.lt.0.or.m.gt.l.or.abs(x).gt.1.d0)pause 'bad arguments'
      pmm=1.d0
      if(m.gt.0) then
        somx2=dsqrt((1.d0-x)*(1.d0+x))
        fact=1.d0
        do 11 i=1,m
           pmm=-pmm*fact*somx2
           fact=fact+2.d0
  11    continue
      end if
      if(l.eq.m) then
        plgndr=pmm
      else
        pmmp1=x*(2*m+1)*pmm
        if(l.eq.m+1) then
           plgndr=pmmp1
        else
           do 12 ll=m+2,l
               pll=(x*(2*ll-1)*pmmp1-(ll+m-1)*pmm)/(ll-m)
               pmm=pmmp1
               pmmp1=pll
  12       continue
         plgndr=pll
        end if
      end if
      return
      end
